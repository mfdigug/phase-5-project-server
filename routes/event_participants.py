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
