from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Event, User, EventParticipant, Restaurant
from datetime import datetime

# Use cases:
# creating an event: POST /api/events
# deleting an event: DELETE /api/events/<id>
# maybe viewing all events/admin testing: GET /api/events


class Events(Resource):
    def get(self):
        
        events = [event.to_dict()
                  for event in Event.query.all()]
        return make_response(jsonify(events), 200)

    def post(self):
        data = request.get_json()

        date_str = data.get("date")
        date_obj = datetime.fromisoformat(date_str)

        event = Event(
            title=data.get("title"),
            date=date_obj,
            cuisine_filter=data.get("cuisine_filter"),
            price_filter=data.get("price_filter"),

            # geo coordinates
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            radius_km=data.get("radius_km"),

            created_by=data.get("created_by"),
        )

        db.session.add(event)
        db.session.commit()

        # set creator automatically to accepted
        creator_id = data.get("created_by")
        participants = []

        participants.append(
            EventParticipant(
                event=event,
                user_id=creator_id,
                rsvp_status="accepted"
            )
        )

        # invitees - set automatically to invited
        invitee_usernames = data.get("invitees", [])
        for username in invitee_usernames:
            user = User.query.filter_by(username=username).first()

            if not user:
                print(f"No user found for username: {username}")
                continue

            if user.id != creator_id:
                participants.append(
                    EventParticipant(
                        event=event,
                        user_id=user.id,
                        rsvp_status="invited"
                    )
                )

        db.session.add_all(participants)
        db.session.commit()

        participants_data = [
            {
                "id": ep.id,
                "user_id": ep.user_id,
                "username": ep.user.username if ep.user else None,
                "rsvp_status": ep.rsvp_status
            }
            for ep in event.participants
        ]

        event_dict = event.to_dict()
        event_dict["participants"] = participants_data

        return make_response(
            jsonify(event_dict), 201
        )

class EventById(Resource):
    def get(self, id):      
        event = Event.query.get(id)

        if not event:
            return {"error": "Event not found"}, 404

        return event.to_dict(), 200

    def delete(self, id):
        user_id = session.get("user_id")
        if not user_id:
            return make_response(jsonify({"error": "Not logged in"}), 401)

        event = Event.query.filter(Event.id == id).first()

        if not event:
            return make_response(jsonify({"error": "Event not found"}), 404)

        if event.created_by != user_id:
            return make_response(jsonify({"error": "Unauthorised"}), 403)

        db.session.delete(event)
        db.session.commit()

        return make_response(jsonify({"message": "Deleted"}), 200)

      

