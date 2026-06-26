from app import api
from .users import *
from .events import Events, EventById
from .event_participants import EventParticipants, EventParticipantById
from .restaurants import Restaurants, RestaurantById
from .user_queries import MyRestaurants, MyEvents
from .generate_restaurant import GenerateRestaurant
from .user_restaurants import UserRestaurants, UserRestaurantById
from .google_places import Autocomplete, PlaceDetails, Places, Photo


# Users
api.add_resource(Users, '/api/users')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')
api.add_resource(CheckSession, '/api/check_session')
api.add_resource(UserById, '/api/users/<int:id>')
api.add_resource(GoogleLogin, '/api/google_login')

# UserQueries
api.add_resource(MyRestaurants, '/api/my_restaurants')
api.add_resource(MyEvents, '/api/my_events')

# GooglePlaces
api.add_resource(Autocomplete, "/api/autocomplete")
api.add_resource(PlaceDetails, "/api/place/<string:place_id>")
api.add_resource(Photo, "/api/photo/<path:photo_name>")
api.add_resource(Places, "/api/places")

# UserRestaurants
api.add_resource(UserRestaurants, '/api/user_restaurants')
api.add_resource(UserRestaurantById, '/api/user_restaurants/<int:id>')

# Events
api.add_resource(Events, '/api/events')
api.add_resource(EventById, '/api/events/<int:id>')

# Generate Restaurant
api.add_resource(GenerateRestaurant, '/api/events/<int:event_id>/generate_restaurant')

# EventParticipants
api.add_resource(EventParticipants, '/api/event_participants')
api.add_resource(EventParticipantById, '/api/event_participants/<int:id>')

# Restaurants
api.add_resource(Restaurants, '/api/restaurants')
api.add_resource(RestaurantById, '/api/restaurants/<int:id>')


