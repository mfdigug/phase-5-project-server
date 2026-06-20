from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Event, User, EventParticipant, Restaurant
import random
import math

class GenerateRestaurant(Resource):
    def post(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return make_response(jsonify({"error": "Event not found"}), 404)
    
        attendees = [
            ep.user for ep in event.participants
            if ep.rsvp_status == "accepted"
        ]

        wishlist_restaurants = []
        for user in attendees:
            for ur in user.user_restaurants:
                if ur.status == "wishlist":
                    restaurant = ur.restaurant
                    if restaurant not in wishlist_restaurants:
                        wishlist_restaurants.append(restaurant)
        
        if not wishlist_restaurants:
            return make_response(
                jsonify({"message": "No wishlist restaurants"}),
                404
            )
        
        def distance_km(lat1, lng1, lat2, lng2):

            R = 6371

            dlat = math.radians(lat2 - lat1)
            dlng = math.radians(lng2 - lng1)

            a = (
                math.sin(dlat / 2) ** 2
                + math.cos(math.radians(lat1))
                * math.cos(math.radians(lat2))
                * math.sin(dlng / 2) ** 2
            )

            return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        scored = []

        for restaurant in wishlist_restaurants:

            score = 0

            if event.price_filter is not None and restaurant.price_level is not None:

                diff = abs(restaurant.price_level - event.price_filter)

                if diff == 0:
                    score += 3
                elif diff == 1:
                    score += 1
                
            if event.cuisine_filter:
                restaurant_cuisines = restaurant.cuisine_tags or []

                if not restaurant_cuisines and restaurant.cuisine_override:
                    restaurant_cuisines = [restaurant.cuisine_override]

                if event.cuisine_filter in restaurant_cuisines:
                    score += 2
            
            if (
                event.latitude is not None
                and event.longitude is not None
                and restaurant.lat is not None
                and restaurant.lng is not None
            ):

                dist = distance_km(
                    event.latitude,
                    event.longitude,
                    restaurant.lat,
                    restaurant.lng
                )

                if dist < 1:
                    score += 3
                elif dist < 5:
                    score += 2
                elif dist < 10:
                    score += 1
                
            score += random.uniform(0, 0.5)

            scored.append((restaurant, score))

            
        best_score = max(score for _, score in scored)
        best_matches = [restaurant for restaurant, score in scored if score == best_score]
        chosen = random.choice(best_matches)

        event.selected_restaurant = chosen
        db.session.commit()

        return make_response(jsonify({
         "chosen": {
            "id": chosen.id,
            "name": chosen.name,
            "cuisine": chosen.cuisine_tags or [chosen.cuisine_override] if chosen.cuisine_override else ["Restaurant"],
            "location": chosen.address,
            "price_level": chosen.price_level,
            # status = next(
            #     ur.status
            #     for ur in user.user_restaurants
            #     if ur.restaurant_id == chosen.id
            # )
        },
        "debug": {
            "attendees": [u.username for u in attendees],
            "wishlist_count": len(wishlist_restaurants),
            "best_score": best_score,
            "candidates": [
                {"name": r.name, "score": s}
                for r, s in scored
            ]
        }
    }), 200)



