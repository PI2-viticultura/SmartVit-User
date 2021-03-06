from settings import load_database_params
from extensions import client
import pymongo
import datetime
import jwt
import os
import bcrypt


class MongoDB():
    def __init__(self):
        """Constructor to model class."""
        if(os.getenv('ENVIRONMENT') != 'developing_local'):
            self.client = client
        else:
            self.params = load_database_params()
            try:
                self.client = pymongo.MongoClient(
                    **self.params, serverSelectionTimeoutMS=10
                )
            except Exception as err:
                print(f'Erro ao conectar no banco de dados: {err}')

    def test_connection(self):
        try:
            self.client.server_info()
            return True
        except Exception as err:
            print(f'Erro ao conectar no banco de dados: {err}')
            return False

    def close_connection(self):
        self.client.close()

    def get_collection(self, collection='user'):
        db = self.client[os.getenv("DBNAME", "smart-dev")]
        return db[collection]

    def insert_one(self, body, collection='user'):
        try:
            collection = self.get_collection(collection)
            return collection.insert_one(body)
        except Exception as err:
            print(f'Erro ao inserir no banco de dados: {err}')
            return False

    def update_one(self, id, body, collection='user'):
        try:
            collection = self.get_collection(collection)

            collection.find_one_and_update(
                {"_id": id},
                {"$set": body}
            )
            return True

        except Exception as err:
            print(f'Erro ao atualizar no banco de dados: {err}')
            return False

    def delete_one(self, identifier):
        try:
            collection = self.get_collection()
            res = collection.delete_one({"id": identifier})
            if res.deleted_count == 1:
                print(f'mensagem {identifier} removida com sucesso')
            else:
                print(f'Erro ao remover a mensagem {identifier}:'
                      ' nenhuma mensagem encontrada para o id')
        except Exception as err:
            print(f'Erro ao deletar no banco de dados: {err}')

    def get_one(self, email, password, collection='user'):
        collection = self.get_collection(collection)
        document = collection.find_one({"email": email, "role": "user"})
        if not (document is None):
            password_doc = document['password']
            password = str(password).encode("utf-8")
            if bcrypt.checkpw(password, password_doc):
                return document
        else:
            return False

    def get_one_admin(self, email, password, collection='user'):
        collection = self.get_collection(collection)
        document = collection.find_one({"email": email, "role": "admin"})
        if not (document is None):
            password_doc = document['password']
            password = str(password).encode("utf-8")
            if bcrypt.checkpw(password, password_doc):
                return document
        else:
            return False

    def get_all(self, collection='user'):
        collection = self.get_collection(collection)
        documents = collection.find()
        return documents

    def encode_auth_token(self, user, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() +
                datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload, os.getenv('SECRET_KEY'), algorithm='HS256'
            )
        except Exception as e:
            return e

    def get_one_winery(self, identifier):
        collection = self.get_collection('winery')
        document = collection.find_one({"_id": identifier})
        return document

    def get_one_user(self, identifier):
        collection = self.get_collection('user')
        document = collection.find_one({"_id": identifier})
        return document
