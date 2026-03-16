from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Restaurant
from sqlalchemy.exc import IntegrityError


# Restaurants
class Restaurants(Resource):
    def get(self):

        restaurants = [restaurant.to_dict()
                       for restaurant in Restaurant.query.all()]

        return make_response(jsonify(restaurants), 200)

    def post(self):
        data = request.get_json()

        try:
            restaurant = Restaurant(
                name=data.get("name"),
                cuisine=data.get("cuisine"),
                location=data.get("location"),
                price_range=data.get("price_range"),
                status=data.get("status", "wishlist"),
                rating=data.get("rating"),
                suggested_by=data.get("suggested_by")
            )

            db.session.add(restaurant)
            db.session.commit()

            return make_response(
                jsonify(restaurant.to_dict()), 201
            )

        except IntegrityError:
            db.session.rollback()

            return make_response(
                jsonify({"error": "You already added this restaurant"}), 400
            )
