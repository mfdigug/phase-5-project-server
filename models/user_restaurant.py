from app import db
from sqlalchemy_serializer import SerializerMixin


class UserRestaurant(db.Model, SerializerMixin):
    __tablename__ = "user_restaurants"

    __table_args__ = (
        db.UniqueConstraint("user_id", "restaurant_id", name="unique_user_restaurant_link"),
    )

    serialize_rules = (
         "-user.user_restaurants",
        "-restaurant.user_restaurants",
    )

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)

    status = db.Column(db.String, default="wishlist")
    personal_rating = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # relationships
    user = db.relationship("User", backref="user_restaurants")
    restaurant = db.relationship("Restaurant", back_populates="user_restaurants")

    def __repr__(self):
        return f"<UserRestaurant user={self.user_id} restaurant={self.restaurant_id}>"


    