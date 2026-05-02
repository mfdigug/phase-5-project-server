from faker import Faker
import random

from app import app, db
from models import (
    User,
    Restaurant,
    Event,
    EventParticipant,
    UserRestaurant
)

fake = Faker()

with app.app_context():
    print("Clearing database...")

    EventParticipant.query.delete()
    UserRestaurant.query.delete()
    Event.query.delete()
    Restaurant.query.delete()
    User.query.delete()

    db.session.commit()

    # -------------------------------------------------
    # USERS (5 only as requested)
    # -------------------------------------------------
    print("Creating users...")

    users = []
    for i in range(5):
        user = User(
            email=fake.unique.email(),
            username=fake.unique.user_name()
        )
        user.set_password("P@ssword00")
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # -------------------------------------------------
    # RESTAURANTS (Google-like canonical data)
    # -------------------------------------------------
    print("Creating restaurants...")

    cuisines = ["Italian", "Japanese", "Mexican", "Thai", "Indian"]

    restaurants = []

    for i in range(15):
        restaurant = Restaurant(
            google_place_id=f"place_{i}_{fake.uuid4()}",

            name=fake.company(),
            address=fake.address(),

            lat=float(fake.latitude()),
            lng=float(fake.longitude()),

            rating=round(random.uniform(3.0, 5.0), 1),
            website=fake.url(),
            photo_refs=[],

            cuisine_override=random.choice(cuisines),
            price_level=random.randint(1, 5)
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    # -------------------------------------------------
    # USER RESTAURANTS (wishlist + tried + ratings)
    # -------------------------------------------------
    print("Creating user restaurants...")

    user_restaurants = []

    for user in users:
        sampled = random.sample(restaurants, 6)

        for r in sampled:
            user_restaurants.append(
                UserRestaurant(
                    user_id=user.id,
                    restaurant_id=r.id,
                    status=random.choice(["wishlist", "tried"]),
                    personal_rating=random.choice([None, 3, 4, 5]),
                    notes=fake.sentence() if random.random() > 0.5 else None
                )
            )

    db.session.add_all(user_restaurants)
    db.session.commit()

    # -------------------------------------------------
    # EVENTS
    # -------------------------------------------------
    print("Creating events...")

    events = []

    for i in range(5):
        creator = random.choice(users)

        event = Event(
            title=fake.catch_phrase(),
            date=fake.date_time_between(start_date="+1d", end_date="+30d"),

            cuisine_filter=random.choice(cuisines),
            price_filter=random.randint(1, 5),

            latitude=float(fake.latitude()),
            longitude=float(fake.longitude()),

            created_by=creator.id
        )

        events.append(event)

    db.session.add_all(events)
    db.session.commit()

    # -------------------------------------------------
    # EVENT PARTICIPANTS
    # -------------------------------------------------
    print("Creating event participants...")

    participants = []

    for event in events:

        # creator always accepted
        participants.append(
            EventParticipant(
                event_id=event.id,
                user_id=event.created_by,
                rsvp_status="accepted"
            )
        )

        # 2–3 invited users
        others = [u for u in users if u.id != event.created_by]
        invitees = random.sample(others, 2)

        for u in invitees:
            participants.append(
                EventParticipant(
                    event_id=event.id,
                    user_id=u.id,
                    rsvp_status=random.choice(["invited", "accepted", "declined"])
                )
            )

    db.session.add_all(participants)
    db.session.commit()

    print("Seeding complete!")