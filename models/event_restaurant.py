from app import db
from sqlalchemy_serializer import SerializerMixin


class EventRestaurant(db.Model, SerializerMixin):
    __tablename__ = "event_restaurants"

    serialize_rules = (
        "-event.event_restaurants",
        "-restaurant.event_restaurants",
    )

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)

    # ranking metadata
    score = db.Column(db.Float, nullable=True)
    is_selected = db.Column(db.Boolean, default=False)

    # relationships
    event = db.relationship("Event", back_populates="event_restaurants")
    restaurant = db.relationship("Restaurant", back_populates="event_restaurants")
