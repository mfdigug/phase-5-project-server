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
