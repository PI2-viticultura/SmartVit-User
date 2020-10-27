from models.user import MongoDB
from flask import jsonify
from flask_jwt_extended import create_access_token
from utils.validators_user import (
    validate_email, validate_password
)


def login_request(request):

    if request:
        email = request["email"]
        password = request["password"]

    if not validate_email(request):
        return {"erro": "Não é possível enviar email vazio"}, 400

    if not validate_password(request):
        return {"erro": "Não é possível enviar senha vazio"}, 400

    db = MongoDB()

    connection_is_alive = db.test_connection()
    if connection_is_alive:
        has_user = db.get_one(email, password)
    if has_user:
        access_token = create_access_token(identity=email)
        return jsonify(
            message="Login Succeeded!",
            access_token=access_token
        ), 201
    else:
        return jsonify(message="Bad Email or Password"), 401
