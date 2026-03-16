from flask import jsonify, make_response, request, session
from flask_restful import Resource
from models import User, Restaurant, Event, EventParticipant
from config import app, db, api
from sqlalchemy.exc import IntegrityError


# Restaurants
class Restaurants(Resource):
    def get(self):

        restaurants = [restaurant.to_dict()
                       for restaurant in Restaurant.query.all()]

        return make_response(jsonify(restaurants), 200)

    def post(self):
        data = request.get_json()

        try:
            restaurant = Restaurant(
                name=data.get("name"),
                cuisine=data.get("cuisine"),
                location=data.get("location"),
                price_range=data.get("price_range"),
                status=data.get("status", "wishlist"),
                rating=data.get("rating"),
                suggested_by=data.get("suggested_by")
            )

            db.session.add(restaurant)
            db.session.commit()

            return make_response(
                jsonify(restaurant.to_dict()), 201
            )

        except IntegrityError:
            db.session.rollback()

            return make_response(
                jsonify({"error": "You already added this restaurant"}), 400
            )


api.add_resource(Restaurants, '/api/restaurants')


# Users
class Users(Resource):
    def get(self):
        users = [user.to_dict()
                 for user in User.query.all()]
        return make_response(jsonify(users), 200)


api.add_resource(Users, '/api/users')


# Register User

class Register(Resource):

    def post(self):
        data = request.get_json()

        try:
            user = User(
                username=data.get("username"),
                email=data.get("email")
            )

            user.set_password(data["password"])

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return make_response(
                jsonify(user.to_dict()), 201
            )

        except IntegrityError:
            db.session.rollback()

            return make_response(
                jsonify(
                    {"error": "A user with this username or email already exists"}), 400
            )


api.add_resource(Register, '/api/register')


# Events
class Events(Resource):
    def get(self):
        events = [event.to_dict()
                  for event in Event.query.all()]
        return make_response(jsonify(events), 200)

    def post(self):
        data = request.get_json()

        event = Event(
            title=data.get("title"),
            date=data.get("date")
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
                        uuser=User.query.get(user_id),
                        rsvp_status="invited"
                    )
                )

        db.session.add_all(participants)
        db.session.commit()

        return make_response(
            jsonify(event.to_dict()), 201
        )


api.add_resource(Events, '/api/events')


# EventPariticpants
class EventParticipants(Resource):
    def get(self):
        event_participants = [event_participant.to_dict()
                              for event_participant in EventParticipant.query.all()]
        return make_response(jsonify(event_participants), 200)


api.add_resource(EventParticipants, '/api/event_participants')
