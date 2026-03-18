from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from sqlalchemy.exc import IntegrityError
from models import User

class Users(Resource):
    def get(self):
        users = [user.to_dict()
                 for user in User.query.all()]
        return make_response(jsonify(users), 200)


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return make_response(jsonify(user.to_dict()), 200)
        return make_response(jsonify({"error": "Unauthorised"}), 401)


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

