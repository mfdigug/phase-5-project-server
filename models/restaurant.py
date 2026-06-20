from app import db
from sqlalchemy_serializer import SerializerMixin


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = (
    "-user_restaurants.restaurant",
    "-event_restaurants.restaurant",
)

    id = db.Column(db.Integer, primary_key=True)

    google_place_id = db.Column(db.String, unique=True, nullable=False)

    # Core google data
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    rating = db.Column(db.Float)
    website = db.Column(db.String)
    price_level = db.Column(db.Integer, nullable=True)
    photo_refs = db.Column(db.JSON)

    cuisine_override = db.Column(db.String, nullable=True)
    cuisine_tags = db.Column(db.JSON, default=list)
    # relationships
    user_restaurants = db.relationship(
        "UserRestaurant",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )
    
    event_restaurants = db.relationship(
        "EventRestaurant",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Restaurant {self.name}>'
