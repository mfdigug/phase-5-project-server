from app import app, api
from .users import Users, Register, Login, Logout, CheckSession
from .events import Events
from .event_participants import EventParticipants
from .restaurants import Restaurants, RestaurantById
from .user_queries import MyRestaurants, MyEvents


# Users
api.add_resource(Users, '/api/users')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(CheckSession, '/api/check_session')

# UserQueries
api.add_resource(MyRestaurants, '/api/my_restaurants')
api.add_resource(MyEvents, '/api/my_events')


# Events
api.add_resource(Events, '/api/events')

# EventParticipants
api.add_resource(EventParticipants, '/api/event_participants')

# Restaurants
api.add_resource(Restaurants, '/api/restaurants')
api.add_resource(RestaurantById, '/api/restaurants/<int:id>')
