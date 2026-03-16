from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import db
from models import Event, User, EventParticipant, Restaurant


class Events(Resource):
    def get(self):
        events = [event.to_dict()
                  for event in Event.query.all()]
        return make_response(jsonify(events), 200)

    def post(self):
        data = request.get_json()

        event = Event(
            title=data.get("title"),
            date=data.get("date"),
            cuisine_filter=data.get("cuisine_filter"),
            location_filter=data.get("location_filter"),
            price_filter=data.get("price_filter"),
            created_by=data.get("created_by"),
            selected_restaurant=None
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
        invitee_ids = data.get("invitees", [])
        for user_id in invitee_ids:
            if user_id != creator_id:
                participants.append(
                    EventParticipant(
                        event=event,
                        user=User.query.get(user_id),
                        rsvp_status="invited"
                    )
                )

        db.session.add_all(participants)
        db.session.commit()

        return make_response(
            jsonify(event.to_dict()), 201
        )
