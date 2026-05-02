from flask import jsonify, make_response, session
from flask_restful import Resource
from models import User, Event, UserRestaurant

class MyRestaurants(Resource):
    def get(self):

        user_id = session.get("user_id")
        if not user_id:
            return make_response(jsonify({"error": "Not logged in"}), 401)

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)


        restaurants = [
            {"restaurant": ur.restaurant.to_dict(),
             "status": ur.status,
             "personal_rating": ur.personal_rating
             }
             for ur in user.user_restaurants
        ]

        return make_response(jsonify(restaurants), 200)

class MyEvents(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return make_response(jsonify({"error": "Not logged in"}), 401)

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        
        created_events = Event.query.filter_by(created_by=user.id).all()

        created_events_data = []
        for e in created_events:
            participants = [
                {"id": ep.id,
                "user_id": ep.user_id,
                "username": ep.user.username if ep.user else None,
                "rsvp_status": ep.rsvp_status}
                for ep in e.participants
            ]
            
            event_dict = e.to_dict()
            event_dict["participants"] = participants
            
            event_dict["selected_restaurant"] = (
                e.selected_restaurant.to_dict()
                if e.selected_restaurant else None
            )
            created_events_data.append(event_dict)

        invited_events = []
        for my_ep in user.event_participants:
            e = my_ep.event
            if e.created_by != int(user_id):
                participants = [
                    {"id": ep.id,
                    "user_id": ep.user_id,
                    "username": ep.user.username if ep.user else None,
                    "rsvp_status": ep.rsvp_status}
                    for ep in e.participants
                ]
                event_dict = e.to_dict()
                event_dict["participants"] = participants
                event_dict["selected_restaurant"] = (
                    e.selected_restaurant.to_dict()
                    if e.selected_restaurant else None
                )
                invited_events.append(event_dict)

        return make_response(
            jsonify({
                "created": created_events_data,
                "invited": invited_events
            }),
            200
        )