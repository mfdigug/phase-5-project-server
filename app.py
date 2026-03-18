import os

from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True
app.json.compact = False

@app.before_request
def check_if_logged_in():
    open_paths = [
        '/api/login',
        '/api/register',
        '/api/check_session'
    ]

    if request.method == "OPTIONS":
        return

    if request.path.startswith("/api") and request.path not in open_paths:
        if not session.get('user_id'):
            return jsonify({"error": "Unauthorized"}), 401

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)

api = Api(app)
import routes