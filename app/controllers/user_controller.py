from models.user import MongoDB
from utils.validators_user import (
    validate_name, validate_cpf, validate_email, validate_password,
    validate_type, validate_situation, validate_fields
)
from bson import ObjectId, json_util
import json
import bcrypt


def save_user_request(request):
    if not validate_fields(request):
        return {
            "erro": "Sua requisição não informou todos os campos necessários"
        }, 400

    if not validate_name(request):
        return {"erro": "Não é possível enviar nome vazio"}, 400

    if not validate_cpf(request):
        return {"erro": "Não é possível enviar cpf vazio"}, 400

    if not validate_email(request):
        return {"erro": "Não é possível enviar email vazio"}, 400
    if not validate_password(request):
        return {"erro": "Não é possível enviar senha vazio"}, 400
    if not validate_type(request):
        return {"erro": "Não é possível enviar tipo vazio"}, 400
    if not validate_situation(request):
        return {"erro": "Não é possível enviar situação vazio"}, 400

    db = MongoDB()

    keyWord = request['password'].encode("utf-8")
    hashed = bcrypt.hashpw(keyWord, bcrypt.gensalt())
    request['password'] = hashed

    connection_is_alive = db.test_connection()
    if connection_is_alive:
        if(db.insert_one(request)):
            return {"message": "Sucess"}, 200

    db.close_connection()

    return {'error': 'Something gone wrong'}, 500


def update_user_request(id, request):
    if not validate_fields(request):
        return {
            "erro": "Sua requisição não informou todos os campos necessários"
        }, 400

    if not validate_name(request):
        return {"erro": "Não é possível enviar nome vazio"}, 400

    if not validate_cpf(request):
        return {"erro": "Não é possível enviar cpf vazio"}, 400

    if not validate_email(request):
        return {"erro": "Não é possível enviar email vazio"}, 400
    if not validate_password(request):
        return {"erro": "Não é possível enviar senha vazio"}, 400
    if not validate_type(request):
        return {"erro": "Não é possível enviar tipo vazio"}, 400
    if not validate_situation(request):
        return {"erro": "Não é possível enviar situação vazio"}, 400

    user_id = ObjectId(id)

    db = MongoDB()
    connection_is_alive = db.test_connection()

    if connection_is_alive:
        if(db.update_one(user_id, request)):
            if(db.update_one(user_id, request, 'user')):
                return {"message": "success"}, 200

    db.close_connection()

    return {'error': 'Something gone wrong'}, 500


def get_users_request():
    db = MongoDB()
    connection_is_alive = db.test_connection()
    if connection_is_alive:
        documents = db.get_all()
        if(documents):
            docs = [doc for doc in documents]
            json_docs = json.dumps(docs, default=json_util.default)
            return json_docs, 200

    db.close_connection()

    return {'error': 'Something gone wrong'}, 500
