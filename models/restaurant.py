from app import db
from sqlalchemy_serializer import SerializerMixin


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    __table_args__ = (
        db.UniqueConstraint("name", "location", "suggested_by",
                            name="unique_user_restaurant"),
    )

    serialize_rules = ("-user.restaurants", "-events.selected_restaurant")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    cuisine = db.Column(db.String)
    location = db.Column(db.String)
    price_range = db.Column(db.String)
    status = db.Column(db.String, default="wishlist")  # 'wishlist' or 'tried'
    rating = db.Column(db.Integer, nullable=True)

    suggested_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="restaurants")

    def __repr__(self):
        return f'<Restaurant {self.name} | Location {self.location} | Cuisine {self.cuisine}>'
