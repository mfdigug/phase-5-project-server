import os

from flask import Flask, request, session, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID") 
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') 
google_bp = make_google_blueprint(scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_to="login_success"
)
app.register_blueprint(google_bp, url_prefix="/login")

app.config['SESSION_COOKIE_SAMESITE'] = "Lax" 
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.json.compact = False

# @app.before_request
# def check_if_logged_in():
#     open_paths = [
#         '/api/login',
#         '/api/register',
#         '/api/check_session'
#     ]

#     if request.method == "OPTIONS":
#         return

#     if request.path.startswith("/api") and request.path not in open_paths:
#         if not session.get('user_id'):
#             return jsonify({"error": "Unauthorised"}), 401

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



api = Api(app)
import routes



@app.route("/login/success")
def login_success():
    session["user_id"] = 123

    print("SESSION AFTER SET:", dict(session))

    return redirect("http://localhost:5173/dashboard")

@app.route("/debug_session")
def debug_session():
    return {
        "session": dict(session),
        "user_id": session.get("user_id")
    }