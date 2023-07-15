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
    return True if (data["phoneNumber"] != None or data["email"] != None) else False


def handle_request(data):
    new_identity = Identity(
        email=data["email"],
        phone_number=data["phoneNumber"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    primary_id = None

    email_exists = email_already_exists(new_identity.email)
    phone_exists = phone_already_exists(new_identity.phone_number)

    primary_identity_email = [
        identity for identity in email_exists if identity.link_precedence == "primary"
    ]
    primary_identity_phone = [
        identity for identity in phone_exists if identity.link_precedence == "primary"
    ]

    if len(primary_identity_email) > 0 and len(primary_identity_phone) > 0:
        operable = [primary_identity_email[0], primary_identity_phone[0]]
        if operable[0].id == operable[1].id:
            Identity.query.filter_by(id=operable[0].id).update(
                dict(
                    updated_at=datetime.now(),
                )
            )
        else:
            operable.sort(key=lambda x: x.created_at, reverse=True)
            primary_id = operable[1].id
            Identity.query.filter_by(id=operable[0].id).update(
                dict(
                    link_precedence="secondary",
                    linked_id=operable[1].id,
                    updated_at=datetime.now(),
                )
            )
    elif len(phone_exists) > 0:
        print("Phone Exists")
        new_identity.link_precedence = "secondary"
        new_identity.linked_id = (
            primary_identity_phone[0].id
            if len(primary_identity_phone) > 0
            else phone_exists[0].linked_id
        )
        add_to_db(new_identity)
    elif len(email_exists) > 0:
        print("Phone Exists")
        new_identity.link_precedence = "secondary"
        new_identity.linked_id = (
            primary_identity_email[0].id
            if len(primary_identity_email) > 0
            else email_exists[0].linked_id
        )
        add_to_db(new_identity)
    else:
        new_identity.link_precedence = "primary"
        add_to_db(new_identity)
    primary_id = new_identity.linked_id
    db.session.commit()
    return primary_id


def generate_response(data, primary_id):
    if primary_id == None:
        primary = (
            Identity.query.filter(
                (Identity.email == data["email"])
                | (Identity.phone_number == data["phoneNumber"])
            )
            .filter_by(link_precedence="primary")
            .first()
        )
    else:
        primary = Identity.query.filter_by(id=primary_id).first()
    secondaries = Identity.query.filter_by(linked_id=primary.id).all()

    return primary.serialize(secondaries)
