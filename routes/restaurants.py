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


class RestaurantById(Resource):
    def get(self, id):
        
        response_dict = Restaurant.query.filter_by(id=id).first().to_dict()
        
        response = make_response(response_dict, 200)
        return response
    
    def patch(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        data = request.get_json()

        for attr in data:
            setattr(restaurant, attr, data[attr])

        db.session.commit()

        return make_response(
            restaurant.to_dict(),
            200
        )
        
    def delete(self, id):
        
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        if not restaurant:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

        db.session.delete(restaurant)
        db.session.commit()

        return make_response(jsonify({"message": "Deleted"}), 200)
