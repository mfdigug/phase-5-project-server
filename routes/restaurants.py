from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Restaurant
from sqlalchemy.exc import IntegrityError

# price string -> int helper
def normalize_google_price_level(price_level):
    price_map = {
        "PRICE_LEVEL_FREE": 1,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }

    if price_level is None:
        return None

    if isinstance(price_level, int):
        return price_level

    return price_map.get(price_level)

# Restaurants
class Restaurants(Resource):
    def get(self):
        
        restaurants = [restaurant.to_dict()
                       for restaurant in Restaurant.query.all()]

        return make_response(jsonify(restaurants), 200)

    def post(self):
        data = request.get_json()

        existing_restaurant = Restaurant.query.filter_by(
            google_place_id=data.get("google_place_id")
            ).first()

        if existing_restaurant:
            return make_response(
                jsonify(existing_restaurant.to_dict()),
                200
            )

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
                photo_refs=[
                    p if isinstance(p, str) else p.get("name")
                    for p in (data.get("photo_refs") or [])
                ][:3],

                # Enrichment fields only
                cuisine_override=data.get("cuisine_override"),
                cuisine_tags=data.get("cuisine_tags"),
                price_level=normalize_google_price_level(data.get("price_level"))
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