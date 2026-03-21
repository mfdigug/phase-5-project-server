from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Event, User, EventParticipant, Restaurant
import random

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
            for restaurant in user.restaurants:
                if restaurant.status == "wishlist" and restaurant not in wishlist_restaurants:
                    wishlist_restaurants.append(restaurant)
        
        if not wishlist_restaurants:
            return make_response(
                jsonify({"message": "No wishlist restaurants"}),
                404
            )

        filtered = [
            restaurant for restaurant in wishlist_restaurants
            if (
                restaurant.price_range == event.price_filter and
                restaurant.cuisine == event.cuisine_filter and
                restaurant.location == event.location_filter
            )
        ]
        

        #selection process
        
        if filtered:
            chosen = random.choice(filtered)
        else:
            scored = []

            for restaurant in wishlist_restaurants:
                score = 0

                price_diff = abs(restaurant.price_range - event.price_filter)
                if price_diff == 0:
                    score += 2
                elif price_diff == 1:
                    score += 1


                if restaurant.cuisine == event.cuisine_filter:
                    score += 1
                if restaurant.location == event.location_filter:
                    score += 1
                
                scored.append((restaurant, score)) #tuple
            
            best_score = max(score for _, score in scored)
            best_matches = [restaurant for restaurant, score in scored if score == best_score]
            chosen = random.choice(best_matches)

        event.selected_restaurant = chosen
        db.session.commit()

        return make_response(jsonify(chosen.to_dict()), 200)



