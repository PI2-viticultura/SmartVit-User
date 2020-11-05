from flask import Blueprint, request
from flask_cors import CORS
import controllers.user_controller as controller
from flask_jwt_extended import jwt_required

app = Blueprint('user', __name__)
CORS(app)


@app.route("/user", methods=["POST"])
def user():
    if request.method == "POST":
        return controller.save_user_request(request.json)


@app.route("/user/<string:id>", methods=["PUT"])
@jwt_required
def user_put(id):
    if request.method == "PUT":
        return controller.update_user_request(id, request.json)


@app.route("/user", methods=["GET"])
def user_get():
    if request.method == "GET":
        return controller.get_users_request()


@app.route("/users/<string:user_id>", methods=["PATCH"])
def user_update_status(user_id):
    return controller.change_status(user_id)

@app.route("/login", methods=["GET"])
def user_login():
    return controller.get_user_login(request.json)