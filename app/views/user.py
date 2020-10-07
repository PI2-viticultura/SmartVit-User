from flask import Blueprint, request
from flask_cors import CORS
import controllers.user_controller as controller

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
