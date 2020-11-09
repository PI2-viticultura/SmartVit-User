from flask import Flask
from flask_cors import CORS
from views.user import app as user
from views.login import app as login
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_KEY", "this-is-secret-key")
app.register_blueprint(user)
app.register_blueprint(login)
CORS(app, automatic_options=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
