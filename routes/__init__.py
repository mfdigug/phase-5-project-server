from app import app, api
from .users import Users, Register, Login, Logout
from .events import Events
from .event_participants import EventParticipants
from .restaurants import Restaurants

# Users
api.add_resource(Users, '/api/users')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')

# Events
api.add_resource(Events, '/api/events')

# EventParticipants
api.add_resource(EventParticipants, '/api/event_participants')

# Restaurants
api.add_resource(Restaurants, '/api/restaurants')
