from models.user import MongoDB
from utils.validators_user import (
    validate_name, validate_cpf, validate_email, validate_password,
    validate_type, validate_situation, validate_fields,
    validate_winery
)
from bson import ObjectId, json_util
import json
import bcrypt
import requests


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
    if not validate_winery(request):
        return {"erro": "Não é possível enviar vinícola vazio"}, 400

    db = MongoDB()

    keyWord = request['password'].encode("utf-8")
    hashed = bcrypt.hashpw(keyWord, bcrypt.gensalt())
    request['password'] = hashed

    connection_is_alive = db.test_connection()
    if connection_is_alive:
        winery_id = ObjectId(request['winery'])
        winery = db.get_one_winery(winery_id)
        if not winery:
            return {'error': 'winery not found'}, 404

        user = db.insert_one(request)
        if user:
            user = db.get_one_user(user.inserted_id)

        if(user):
            if 'responsibles' not in winery.keys():
                winery['responsibles'] = []

            elif not winery['responsibles']:
                winery['responsibles'] = []

            winery['responsibles'].append(user)

            if(db.update_one(winery_id, winery, 'winery')):
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
    if not validate_winery(request):
        return {"erro": "Não é possível enviar vinícola vazio"}, 400

    user_id = ObjectId(id)

    db = MongoDB()

    key_word = request['password'].encode("utf-8")
    hashed = bcrypt.hashpw(key_word, bcrypt.gensalt())
    request['password'] = hashed

    connection_is_alive = db.test_connection()

    if connection_is_alive:
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


def change_status(user_id):
    notification_api = ("https://smartvit-notification-dev.herokuapp.com/" +
                        "user-notification")
    data = dict()
    id_transformed = ObjectId(user_id)
    db = MongoDB()
    active_user = ("Sua conta na SmartVit foi ativada e você já pode começar" +
                   "a usar nosso sistema!")

    connection_is_alive = db.test_connection()
    if connection_is_alive:

        user = db.get_one(id_transformed, 'user')

        if user:
            if 'situation' not in user.keys():
                user['situation'] = 1
            elif (user['situation'] == 1):
                active_user = "Sua conta na SmartVit foi desativada!"
                user['situation'] = 0
            else:
                user['situation'] = 1

            retorno = db.update_one(id_transformed, user)

            data['type'] = 'user'
            data['title'] = "Conta"
            data['message'] = active_user
            data['users_ids'] = [str(user['_id'])]
            data['emails'] = [user['email']]

            requests.post(notification_api, json=data)

            if retorno:
                return {'message': 'Success'}, 200

    return {'message': 'Something gone wrong'}, 500


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
            return {'message': 'Sem usuário'}, 400
