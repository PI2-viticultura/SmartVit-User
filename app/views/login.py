from flask import Blueprint, request
from flask_cors import CORS
import controllers.login_controller as controller


app = Blueprint('login', __name__)
CORS(app)


@app.route("/login", methods=["POST"])
def user_login():
    return controller.login_request(request.json)
