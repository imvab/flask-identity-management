from .extensions import db
from .models import Identity
from datetime import datetime

def email_already_exists(email):
    identities = Identity.query.filter_by(email=email).all()
    return identities if len(identities) > 0 else []

def phone_already_exists(phone):
    identities = Identity.query.filter_by(phone_number=phone).all()
    return identities if len(identities) > 0 else []

def add_to_db(identity):
    db.session.add(identity)

def validate_request(data):
    return True if (data['phoneNumber'] != None or data['email'] != None) else False

def handle_request(data):
    new_identity = Identity(
        email = data['email'],
        phone_number = data['phoneNumber'],
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    email_exists = email_already_exists(new_identity.email)
    phone_exists = phone_already_exists(new_identity.phone_number)

    primary_identity_email = [identity for identity in email_exists if identity.link_precedence == 'primary']
    primary_identity_phone = [identity for identity in phone_exists if identity.link_precedence == 'primary']


    if (len(primary_identity_email) > 0 and len(primary_identity_phone) > 0):
        operable = [primary_identity_email[0], primary_identity_phone[0]]
        operable.sort(key=lambda x: x.created_at, reverse=True)

        Identity.query.filter_by(id=operable[0].id).update(dict(link_precedence='secondary',linked_id=operable[1].id,updated_at=datetime.now()))
    elif len(phone_exists) > 0:
        primary_identity = Identity.query.filter_by(phone_number=new_identity.phone_number,link_precedence='primary').first()
        new_identity.link_precedence = 'secondary'
        new_identity.linked_id = primary_identity.id

        add_to_db(new_identity)
    elif len(email_exists) > 0:
        primary_identity = Identity.query.filter_by(email=new_identity.email,link_precedence='primary').first()
        new_identity.link_precedence = 'secondary'
        new_identity.linked_id = primary_identity.id

        add_to_db(new_identity)
    else:
        new_identity.link_precedence = 'primary'
        add_to_db(new_identity)
        
    db.session.commit()