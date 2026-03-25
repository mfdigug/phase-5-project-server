from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db, app
from sqlalchemy.exc import IntegrityError
from models import User
from flask_dance.contrib.google import google
from flask import redirect, url_for

class Users(Resource):
    def get(self):
        users = [user.to_dict()
                 for user in User.query.all()]
        return make_response(jsonify(users), 200)


class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        return make_response(jsonify(user.to_dict()), 200)


class CheckSession(Resource):
    def get(self):
        
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "Unauthorised"}, 401

        user = User.query.get(user_id)
        return user.to_dict(), 200


class Register(Resource):

    def post(self):
        data = request.get_json()

        try:
            user = User(
                username=data.get("username"),
                email=data.get("email")
            )

            user.set_password(data["password"])

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return make_response(
                jsonify(user.to_dict()), 201
            )

        except IntegrityError:
            db.session.rollback()

            return make_response(
                jsonify(
                    {"error": "A user with this username or email already exists"}), 400
            )
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response(jsonify({"error": "Email and password required"}), 400)
        
        user = User.query.filter(User.email == email).first()
            
        if not user or not user.authenticate(password):
            return make_response(jsonify({"error": "Invalid credentials"}), 401)
        
        
        session['user_id'] = user.id

        return make_response(jsonify(user.to_dict()), 200)
    
class Logout(Resource):

    def delete(self):

        session.pop('user_id', None)
        
        return {}, 204
    


@app.route("/api/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    response = google.get("/oauth2/v1/userinfo")
    user_info = response.json()
    base_username = user_info["email"].split("@")[0]

    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        username = base_username
        user = User(
            username=username,
            email=user_info["email"]
        )

        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id

    return redirect("http://localhost:5173/dashboard")