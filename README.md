# Dinner Decider

## Overview

Dinner Decider is a full-stack application designed to solve a common problem: deciding where to go out for dinner with friends. Many groups of friends want to explore new restaurants but struggle to remember options, reach consensus, or keep track of places they've already tried. Dinner Decider simplifies this process by allowing users to:

- Create a wishlist of restaurants to try
- Mark and rate tried restuarants
- Create dinner plans with friends
- Track RSVP status for each invitee
- Randomly generate a restaurant for the event from a pool of users' wishlisted restaurants and filters

The app combines **React** on the frontend with a **Flask** backend, integrating **Google Authentication**, dynamic state management, and responsive UI design to create a seamless social planning experience.

This is the repo and code for the Flask backend.
You will be able to find the front end repo here: [GitHub Repo Phase 5 Project Client](https://github.com/mfdigug/phase-5-project-client)

You can also find a demo video here: [DinnerDecider App Demo](https://youtu.be/BIpvjqThPIo)

---

## Table of Contents

1. [Tech Stack](#tech-stack)  
2. [Features](#features)  
3. [Setup & Installation](#setup--installation)  
4. [Folder Structure](#folder-structure)  
5. [Key Technical Challenges](#key-technical-challenges)  
6. [Usage](#usage)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## Tech Stack

**Frontend:**

- React (functional components, hooks)  
- React Router for navigation  
- Context API for global state management  
- FontAwesome for icons  
- Custom hooks for events, invitees, and RSVP handling  

**Backend:**

- Flask RESTful API  
- SQLAlchemy ORM with Flask-Migrate  
- Flask-Bcrypt for password hashing  
- Flask-CORS for cross-origin requests  
- Flask-Dance for Google OAuth  

**Database:**

- PostgreSQL (production)  
- SQLite (local development)  

**Authentication:**

- Email/password login  
- Google OAuth login 

**Deployment Considerations:**

- Secure cookie management for Safari/iOS  
- Handling CORS preflight requests for login and data fetching  

---

## Features

### Track Restaurants

- Add new restaurants to your wishlist
- View wishlisted restaurants
- Mark restaurants as tried and rate them for your personal reference

### Dinner Planning

- Create Events and set restaurant filters
- Invite friends to events using autocomplete search   
- "Generate Restaurant" button to generates a random restaurant selection based on attendees wishlisted restaurants and event restaurant filters

### RSVP Tracking & Event views

- RSVP options: "Invited", "Accepted", "Declined 
- Real-time updates reflected in the frontend  
- Separate handling for events you created vs. events you were invited to  

---

## Setup & Installation

### Backend

```bash
# Clone repository
git clone <repo_url>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL=<your_database_url>
export GOOGLE_CLIENT_ID=<your_google_client_id>
export GOOGLE_CLIENT_SECRET=<your_google_client_secret>
export SECRET_KEY=<your_secret_key>


# Initialize database locally
flask db init
flask db migrate
flask db upgrade

# Seed with false data
python seed.py

# Run Flask server
flask run