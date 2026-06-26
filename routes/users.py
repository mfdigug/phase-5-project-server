import os
from flask import jsonify, make_response, request, session, redirect, url_for
from flask_restful import Resource
from app import db
from sqlalchemy.exc import IntegrityError
from models import User
from flask_dance.contrib.google import google

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

class Users(Resource):
    def get(self):
        search = request.args.get("search", "").strip()
        query = User.query
        if search:
            query = query.filter(User.username.ilike(f"%{search}%"))
        users = query.all()
        return jsonify([{"id": u.id, "username": u.username} for u in users])

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        return make_response(jsonify(user.to_dict()), 200)
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": f"User {id} deleted successfully"}), 200)


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
            username=data.get("username")
            email=data.get("email")
            password=data.get("password")
            
            if not username or not email or not password:
                return make_response(
                jsonify({"error": "All fields are required"}), 400
                )
            
            if User.query.filter_by(username=username).first():
                return make_response(
                    jsonify({"error": "Username already exists"}), 400
                )

            if User.query.filter_by(email=email).first():
                return make_response(
                    jsonify({"error": "Email already registered"}), 400
                )
            
            user = User(
                username=username,
                email=email
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
                jsonify({"error": "Username or email already exists"}), 400
            )
        
        except Exception as e:
            db.session.rollback()

            return make_response(
                jsonify({"error": "Something went wrong"}), 500
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

        session.clear()
        
        return {}, 204


class GoogleLogin(Resource):
    def get(self):
        return redirect(f"{BACKEND_URL}/login/google")
        
