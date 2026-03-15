from config import db
from sqlalchemy_serializer import SerializerMixin


class EventParticipant(db.Model, SerializerMixin):
    __tablename__ = "event_participants"
    __table_args__ = (
        db.UniqueConstraint("event_id", "user_id",
                            name="unique_event_participant"),
    )

    serialize_rules = ("-event.participants",
                       "-user.event_participants", "-user.restaurants")

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))

    user = db.relationship("User", back_populates="event_participants")
    event = db.relationship("Event", back_populates="participants")

    rsvp_status = db.Column(db.String)  # 'invited', 'accepted', 'declined'

    def __repr__(self):
        return f'<EventParticipant: {self.user_id} | Event {self.event_id} | RSVP Status: {self.rsvp_status}>'
