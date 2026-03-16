from flask import jsonify, make_response, request, session
from flask_restful import Resource
from app import app, db, api


# EventPariticpants
class EventParticipants(Resource):
    def get(self):
        event_participants = [event_participant.to_dict()
                              for event_participant in EventParticipant.query.all()]
        return make_response(jsonify(event_participants), 200)


api.add_resource(EventParticipants, '/api/event_participants')
