from app import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    serialize_rules = ("-participants.event", "-participants.user.events_created")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    # takes date fromReact frontend (string ISO 8601 format, e.g., "2026-03-15T14:30" handle formatting date in route).
    cuisine_filter = db.Column(db.String)
    price_filter = db.Column(db.Integer)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # relationships

    event_restaurants = db.relationship(
    "EventRestaurant",
    back_populates="event",
    cascade="all, delete-orphan"
    )
    
    participants = db.relationship(
        "EventParticipant",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    creator = db.relationship(
    "User",
    back_populates="events_created"
    )

    def __repr__(self):
        return f'<Event {self.title} | Lat {self.latitude} | Lng {self.longitude} | Cuisine {self.cuisine_filter} | Price {self.price_filter}>'
