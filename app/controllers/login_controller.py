from models.user import MongoDB
from flask import jsonify
from flask_jwt_extended import create_access_token
from utils.validators_user import (
    validate_email, validate_password
)
from bson import json_util
import json


def login_request(request):

    if request:
        email = request["email"]
        password = request["password"]
        role = request["role"]

    if not validate_email(request):
        return {"erro": "Não é possível enviar email vazio"}, 400

    if not validate_password(request):
        return {"erro": "Não é possível enviar senha vazio"}, 400

    db = MongoDB()

    connection_is_alive = db.test_connection()
    if connection_is_alive:
        if role == "admin":
            has_user = db.get_one_admin(email, password)
        else:
            has_user = db.get_one(email, password)
    if has_user:
        access_token = create_access_token(identity=email)
        return jsonify(
            message="Login Succeeded!",
            access_token=access_token
        ), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


def get_user_login(request):
    if not validate_email(request):
        return {"erro": "Não é possível enviar email vazio"}, 400
    if not validate_password(request):
        return {"erro": "Não é possível enviar senha vazio"}, 400
    db = MongoDB()
    connection_is_alive = db.test_connection()
    if connection_is_alive:
        has_user = db.get_one(request['email'], request['password'])
        if has_user:
            has_user.pop('password')
            json_docs = json.dumps(has_user, default=json_util.default)
            return json_docs, 201
        else:
            return {'message': 'Unauthorized'}, 401
