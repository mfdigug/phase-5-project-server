from faker import Faker
import random

from config import app, db
from models import User, Restaurant, Event, EventParticipant

fake = Faker()


with app.app_context():

    print("Clearing database...")

    EventParticipant.query.delete()
    Event.query.delete()
    Restaurant.query.delete()
    User.query.delete()

    db.session.commit()

    print("Creating users...")

    users = []

    for _ in range(15):
        user = User(
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            password_hash="password"
        )

        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating restaurants...")

    restaurants = []

    cuisines = [
        "Italian",
        "Japanese",
        "Mexican",
        "Thai",
        "Indian",
        "Chinese",
        "Greek",
        "Korean"
    ]

    for user in users:
        for _ in range(5):

            restaurant = Restaurant(
                name=fake.company(),
                cuisine=random.choice(cuisines),
                location=fake.city(),
                price_range=random.choice(["$", "$$", "$$$"]),
                status="wishlist",
                suggested_by=user.id
            )

            restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    print("Creating events...")

    events = []

    for _ in range(10):

        creator = random.choice(users)

        event = Event(
            title=fake.catch_phrase(),
            date=fake.date_time_between(start_date="+1d", end_date="+30d"),
            cuisine_filter=random.choice(cuisines),
            location_filter=fake.city(),
            price_filter=random.randint(1, 3),
            created_by=creator.id
        )

        events.append(event)

    db.session.add_all(events)
    db.session.commit()

    print("Creating participants...")

    statuses = ["accepted", "declined", "invited"]

    participants = []

    for event in events:

        creator = event.created_by

        # creator automatically attending
        participants.append(
            EventParticipant(
                event_id=event.id,
                user_id=creator,
                rsvp_status="accepted"
            )
        )

        invited_users = random.sample(users, 2)

        for user in invited_users:

            if user.id != creator:

                participant = EventParticipant(
                    event_id=event.id,
                    user_id=user.id,
                    rsvp_status=random.choice(statuses)
                )

                participants.append(participant)

    db.session.add_all(participants)
    db.session.commit()

    print("Seeding complete!")
