from flask import Blueprint, redirect, url_for, request, Response
from datetime import datetime

from .extensions import db
from .models import Identity
from.utils import handle_request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    identities = Identity.query.all()
    list_html = [f"<li>{ identity.id }</li>" for identity in identities]
    return f"<ul>{''.join(list_html)}</ul>"

@main.route('/identity', methods = ['POST'])
def create_identity():
    data = request.json
    if (validate_request(data)):
        handle_request(data)
        return "Identity Added"
    else:
        return Response("Request Invalid", status=400)
