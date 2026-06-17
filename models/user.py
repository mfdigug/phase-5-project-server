from app import db, bcrypt
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = (
    "-password_hash",
    "-event_participants.user",
    "-events_created.creator",
    "-user_restaurants.user",
)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)   # for email/password login


    # relationships
    event_participants = db.relationship("EventParticipant",
                                         back_populates="user",
                                         cascade="all, delete-orphan"
                                         )
    
    events_created = db.relationship(
    "Event",
    back_populates="creator"
)

    # password hashing

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username} | email {self.email}'
