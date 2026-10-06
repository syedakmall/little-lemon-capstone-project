Little Lemon Capstone Project
=============================

Hi reviewer, thanks for taking the time to grade this project.

SETUP
-----
1. Create a MySQL database:
       CREATE DATABASE littlelemon;
   The connection defaults to user "root" with no password on 127.0.0.1:3306.
   To use other credentials, set MYSQL_USER and MYSQL_PASSWORD
   (see .env.example). MySQL settings are in littlelemon/settings.py.

2. Install and run:
       python -m venv .venv
       source .venv/bin/activate        (Windows: .venv\Scripts\activate)
       pip install -r requirements.txt
       python manage.py migrate
       python manage.py loaddata menu   (adds sample menu items)
       python manage.py createsuperuser
       python manage.py runserver

3. Run the unit tests:
       python manage.py test

GRADING CHECKLIST
-----------------
Static HTML content    /restaurant/
MySQL database         littlelemon/settings.py (DATABASES)
Menu API               /restaurant/menu/
Table booking API      /restaurant/booking/tables/
Registration and auth  /auth/users/ and /api-token-auth/ (Djoser and DRF tokens)
Unit tests             restaurant/tests/

API PATHS TO TEST (Insomnia)
----------------------------
All menu and booking endpoints require authentication.

Register a user
    POST   /auth/users/                         body: username, password

Get a token (either endpoint works)
    POST   /api-token-auth/                     body: username, password
    POST   /auth/token/login/                   body: username, password

Then add this header to every request below:
    Authorization: Token <your token>

Menu
    GET    /restaurant/menu/                    list items (?search=pasta, ?ordering=price)
    POST   /restaurant/menu/                    create item (staff users only)
    GET    /restaurant/menu/<id>/               single item
    PUT    /restaurant/menu/<id>/               update item (staff users only)
    DELETE /restaurant/menu/<id>/               delete item (staff users only)

    Example body: {"title": "Soup", "price": "6.50", "inventory": 10}

Table bookings
    GET    /restaurant/booking/tables/          list bookings
    POST   /restaurant/booking/tables/          create booking
    GET    /restaurant/booking/tables/<id>/     single booking
    PUT    /restaurant/booking/tables/<id>/     update booking
    DELETE /restaurant/booking/tables/<id>/     delete booking

    Example body: {"name": "Jane", "number_of_guests": 4, "booking_date": "2030-01-15T19:00:00"}

Use the superuser account to test the staff-only menu writes.

You can also test everything in the browser using DRF's browsable API.
Log in at /api-auth/login/, then open any of the paths above.

WEBSITE PAGES
-------------
/restaurant/                  Home
/restaurant/about/            About
/restaurant/our-menu/         Menu
/restaurant/book/             Book a table
/restaurant/reservations/     Reservations (staff login required)
/admin/                       Django admin
