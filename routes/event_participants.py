from flask import jsonify, make_response, request, session
from flask_restful import Resource
from models import EventParticipant
from app import db


# EventPariticpants
class EventParticipants(Resource):
    def get(self):
        event_participants = [event_participant.to_dict()
                              for event_participant in EventParticipant.query.all()]
        return make_response(jsonify(event_participants), 200)

class EventParticipantById(Resource):
    def get(self, id):
        user_id = session.get(user_id)
        if not user_id:
            return make_response(jsonify({"error": "Not logged in"}), 401)

        ep = EventParticipant.query.get(id)
        if not ep:
            return make_response(jsonify({"error": "Event participant not found"}), 404)

        if ep.user_id != user_id:
            return make_response(jsonify({"error": "Forbidden"}), 403)

        data = request.get_json()
        for attr in data:
            setattr(ep, attr, date[attr])

        db.session.commit()

        return make_response(ep.to_dict(), 200)
