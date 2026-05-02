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
                # Google Places identity
                google_place_id=data.get("google_place_id"),

                # Core fields
                name=data.get("name"),
                address=data.get("address"),
                lat=data.get("lat"),
                lng=data.get("lng"),

                rating=data.get("rating"),
                website=data.get("website"),
                photo_refs=data.get("photo_refs"),

                # Enrichment fields only
                cuisine_override=data.get("cuisine_override"),
                price_level=data.get("price_level")
            )

            db.session.add(restaurant)
            db.session.commit()

            return make_response(
                jsonify(restaurant.to_dict()), 201
            )

        except IntegrityError:
            db.session.rollback()

            return make_response(
                jsonify({"error": "Restaurant already exists (google_place_id conflict)"}), 400
            )


class RestaurantById(Resource):
    def get(self, id):
        
        response_dict = Restaurant.query.filter_by(id=id).first().to_dict()
        
        response = make_response(response_dict, 200)
        return response