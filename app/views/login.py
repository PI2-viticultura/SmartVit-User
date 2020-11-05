from flask import Blueprint, request
from flask_cors import CORS
import controllers.login_controller as controller


app = Blueprint('login', __name__)
CORS(app)


@app.route("/login", methods=["GET"])
def user_login():
    return controller.get_user_login(request.json)
