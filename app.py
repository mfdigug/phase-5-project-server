import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_restful import Api
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID") 
# app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') 
# google_bp = make_google_blueprint(scope=[
#         "openid",
#         "https://www.googleapis.com/auth/userinfo.email",
#         "https://www.googleapis.com/auth/userinfo.profile"
#     ],
#     redirect_to="login_success"
# )
# app.register_blueprint(google_bp, url_prefix="/login")

app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True


app.json.compact = False


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

CORS(app, 
    supports_credentials=True, 
    origins=["http://localhost:5173", "http://127.0.0.1:5173"])


api = Api(app)



# @app.route("/login/success")
# def login_success():
#     if not google.authorized:
#         return redirect("https://reliable-kataifi-750975.netlify.app/login")

#     resp = google.get("/oauth2/v2/userinfo")
#     user_info = resp.json()
#     email = user_info.get("email")
#     username = email.split("@")[0]

#     from models import User

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         user = User(
#             email=email,
#             username=username
#         )
#         db.session.add(user)
#         db.session.commit()

#     session["user_id"] = user.id

#     return redirect("https://reliable-kataifi-750975.netlify.app/dashboard/restaurants/wishlist")


import routes