from flask import jsonify, make_response, session
from flask_restful import Resource
from models import User, Event

class MyRestaurants(Resource):
    def get(self):

        user_id = session.get("user_id")
        if not user_id:
            return make_response(jsonify({"error": "Not logged in"}), 401)

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

    
        restaurants = [r.to_dict() for r in user.restaurants]

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
                {"user_id": ep.user_id, "rsvp_status": ep.rsvp_status}
                for ep in e.participants
            ]
            event_dict = e.to_dict()
            event_dict["participants"] = participants
            created_events_data.append(event_dict)

        invited_events = []
        for ep in user.event_participants:
            e = ep.event
            if e.created_by != int(user_id):
                participants = [
                    {"user_id": p.user_id, "username": p.user.username if p.user else None, "rsvp_status": p.rsvp_status}
                    for p in e.participants
                ]
                event_dict = e.to_dict()
                event_dict["participants"] = participants
                invited_events.append(event_dict)

        return make_response(
            jsonify({
                "created": created_events_data,
                "invited": invited_events
            }),
            200
        )