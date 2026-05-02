from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import UserRestaurant


class UserRestaurants(Resource):

    # POST → add restaurant to user list
    def post(self):

        user_id = session.get("user_id")

        if not user_id:
            return make_response({"error": "Not logged in"}, 401)

        data = request.get_json()

        restaurant_id = data.get("restaurant_id")

        if not restaurant_id:
            return make_response({"error": "restaurant_id required"}, 400)

        # prevent duplicates (your DB constraint also enforces this)
        existing = UserRestaurant.query.filter_by(
            user_id=user_id,
            restaurant_id=restaurant_id
        ).first()

        if existing:
            return make_response({"error": "Already exists"}, 400)

        ur = UserRestaurant(
            user_id=user_id,
            restaurant_id=restaurant_id,
            status=data.get("status", "wishlist"),
            personal_rating=data.get("personal_rating"),
            notes=data.get("notes")
        )

        db.session.add(ur)
        db.session.commit()

        return make_response(ur.to_dict(), 201)


# for user specific changes to restaurant data
class UserRestaurantById(Resource):

    # PATCH 
    def patch(self, id):

        user_id = session.get("user_id")

        if not user_id:
            return make_response({"error": "Not logged in"}, 401)

        ur = UserRestaurant.query.get(id)

        if not ur:
            return make_response({"error": "Not found"}, 404)

        if ur.user_id != user_id:
            return make_response({"error": "Forbidden"}, 403)

        data = request.get_json()

        allowed_fields = {
            "status",
            "personal_rating",
            "notes"
        }

        for key in data:
            if key in allowed_fields:
                setattr(ur, key, data[key])

        db.session.commit()

        return make_response(ur.to_dict(), 200)


    # DELETE → remove relationship (NOT restaurant itself)
    def delete(self, id):

        user_id = session.get("user_id")

        if not user_id:
            return make_response({"error": "Not logged in"}, 401)

        ur = UserRestaurant.query.get(id)

        if not ur:
            return make_response({"error": "Not found"}, 404)

        if ur.user_id != user_id:
            return make_response({"error": "Forbidden"}, 403)

        db.session.delete(ur)
        db.session.commit()

        return make_response({"message": "Deleted"}, 200)