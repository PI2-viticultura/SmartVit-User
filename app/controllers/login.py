from models.user import MongoDB
from flask import jsonify
from flask_jwt_extended import create_access_token


def login_request(request):

    if request:
        email = request["email"]
        password = request["password"]

    db = MongoDB()

    print(email)
    connection_is_alive = db.test_connection()
    print(connection_is_alive)
    if connection_is_alive:
        hasUser = db.get_one
        (
            {
                "email": email,
                "password": password
            }
        )
        print(hasUser)
    if hasUser:
        print(email)
        access_token = create_access_token(identity=email)
        return jsonify(
            message="Login Succeeded!",
            access_token=access_token
        ), 201
    else:
        return jsonify(message="Bad Email or Password"), 401
