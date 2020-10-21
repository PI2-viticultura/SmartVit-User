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
def user_put(id):
    if request.method == "PUT":
        return controller.update_user_request(id, request.json)


@app.route("/user", methods=["GET"])
@jwt_required
def user_get():
    if request.method == "GET":
        return controller.get_users_request()
