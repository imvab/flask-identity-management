from flask import Blueprint, redirect, url_for, request
from datetime import datetime

from .extensions import db
from .models import Identity

main = Blueprint('main', __name__)

@main.route('/')
def index():
    identities = Identity.query.all()
    list_html = [f"<li>{ identity.id }</li>" for identity in identities]
    return f"<ul>{''.join(list_html)}</ul>"

@main.route('/identity', methods = ['POST'])
def create_identity():
    data = request.json
    new_identity = Identity(
        phone_number = data['phoneNumber'],
        email = data['email'],
        created_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.session.add(new_identity)
    db.session.commit()
    return "Identity Added"
