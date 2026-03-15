from config import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    serialize_rules = ("-participants.event",)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    # takes date fromReact frontend (string ISO 8601 format, e.g., "2026-03-15T14:30" handle formatting date in route).
    cuisine_filter = db.Column(db.String)
    location_filter = db.Column(db.String)
    price_filter = db.Column(db.Integer)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    selected_restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id")
    )

    selected_restaurant = db.relationship("Restaurant")

    participants = db.relationship(
        "EventParticipant",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Event {self.title} | Location {self.location_filter} | Cuisine {self.cuisine_filter} | Price {self.price_filter}>'
