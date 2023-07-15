from .extensions import db
from .models import Identity
from datetime import datetime

def email_already_exists(email):
    identities = Identity.query.filter_by(email=email).all()
    return identities if len(identities) > 0 else False

def phone_already_exists(phone):
    identities = Identity.query.filter_by(phone_number=phone).all()
    return identities if len(identities) > 0 else False

def add_to_db(identity):
    db.session.add(identity)

def handle_request(data):
    new_identity = Identity(
        email = data['email'],
        phone_number = data['phoneNumber'],
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    email_exists = email_already_exists(new_identity.email)
    phone_exists = phone_already_exists(new_identity.phone_number)

    if phone_exists:
        primary_identity = Identity.query.filter_by(phone_number=new_identity.phone_number,link_precedence='primary').first()
        new_identity.link_precedence = 'secondary'
        new_identity.linked_id = primary_identity.id

        add_to_db(new_identity)
    elif email_exists:
        primary_identity = Identity.query.filter_by(email=new_identity.email,link_precedence='primary').first()
        new_identity.link_precedence = 'secondary'
        new_identity.linked_id = primary_identity.id

        add_to_db(new_identity)
    else:
        new_identity.link_precedence = 'primary'
        add_to_db(new_identity)
        
    db.session.commit()