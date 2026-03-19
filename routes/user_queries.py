from flask import jsonify, make_response, session
from flask_restful import Resource
from models import User, Event

class MyRestaurants(Resource):
    def get(self):

        user_id = session.get("user_id") or 1

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

    
        restaurants = [r.to_dict() for r in user.restaurants]

        return make_response(jsonify(restaurants), 200)

class MyEvents(Resource):
    def get(self):
        user_id = session.get("user_id") or 1

        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        created_events = []
        for e in user.events_created:
            participants = [
                {"user_id": ep.user_id, "rsvp_status": ep.rsvp_status}
                for ep in e.participants
            ]
            event_dict = e.to_dict()
            event_dict["participants"] = participants
            created_events.append(event_dict)

        invited_events = []
        for ep in user.event_participants:
            e = ep.event
            if e.created_by != user_id:
                participants = [
                    {"user_id": p.user_id, "username": p.user.username, "rsvp_status": p.rsvp_status}
                    for p in e.participants
                ]
                event_dict = e.to_dict()
                event_dict["participants"] = participants
                invited_events.append(event_dict)

        return make_response(
            jsonify({
                "created": created_events,
                "invited": invited_events
            }),
            200
        )