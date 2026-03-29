from faker import Faker
import random

from app import app, db
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
            username=fake.unique.user_name()
        )
        user.set_password("P@ssword00")
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Creating restaurants...")
    restaurants = []
    cuisines = ["Italian", "Japanese", "Mexican",
                "Thai", "Indian", "Chinese", "Greek", "Korean"]

    for user in users:
        for _ in range(5):
            restaurant = Restaurant(
                name=fake.company(),
                cuisine=random.choice(cuisines),
                location=fake.city(),
                price_range=random.randint(1, 5),
                status="wishlist",
                rating=random.randint(1, 5),
                user=user,
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
            price_filter=random.randint(1, 5),
            created_by=creator.id
        )
        events.append(event)

    db.session.add_all(events)
    db.session.commit()

    print("Creating participants...")
    statuses = ["accepted", "declined", "invited"]
    participants = []

    for event in events:
        # creator automatically attending
        creator_user = User.query.get(event.created_by)
        participants.append(
            EventParticipant(
                event=event,
                user=creator_user,
                rsvp_status="accepted"
            )
        )

        # 2 random invitees not the creator
        invitee_users = random.sample(
            [u for u in users if u.id != event.created_by], 2)
        for user in invitee_users:
            participants.append(
                EventParticipant(
                    event=event,
                    user=user,
                    rsvp_status="invited"
                )
            )

    db.session.add_all(participants)
    db.session.commit()

    print("Seeding complete!")
