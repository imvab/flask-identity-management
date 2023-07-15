from flask import Blueprint, request, jsonify

from .models import Identity
from .utils import handle_request, validate_request, generate_response

main = Blueprint("main", __name__)


@main.route("/")
def index():
    identities = Identity.query.all()
    list_html = [
        f"<li>{ identity.id } { identity.email } { identity.phone_number }</li>"
        for identity in identities
    ]
    return f"<ul>{''.join(list_html)}</ul>"


@main.route("/identity", methods=["POST"])
def create_identity():
    data = request.json
    if validate_request(data):
        primary_id = handle_request(data)
        return jsonify(generate_response(data, primary_id)), 201
    else:
        return jsonify({"msg": "Invalid Params"}), 400
