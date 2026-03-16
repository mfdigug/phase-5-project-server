from app import app, api
from .users import Users, Register
from .events import Events
from .event_participants import EventParticipants
from .restaurants import Restaurants

# Users
api.add_resource(Users, '/api/users')
api.add_resource(Register, '/api/register')

# Events
api.add_resource(Events, '/api/events')

# EventParticipants
api.add_resource(EventParticipants, '/api/event_participants')

# Restaurants
api.add_resource(Restaurants, '/api/restaurants')
