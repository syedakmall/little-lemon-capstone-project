# Little Lemon Capstone Project

Back-end for Little Lemon, a Mediterranean restaurant in Chicago, built with Django and Django REST Framework for the Meta Back-End Developer capstone.

It includes a server-rendered website for guests and a token-authenticated REST API for the menu and table bookings.

## Features

- Website pages: home, about, menu, menu item detail and an online booking form
- Staff-only reservations page with a per-day booking view
- REST API for menu items and table bookings, with search and ordering
- User registration and token login through Djoser
- Menu writes limited to staff accounts; all API reads require authentication
- Validation for party size (1–12 guests) and future-only booking dates
- Request throttling for anonymous and authenticated users
- MySQL support through environment variables, with SQLite as the local default

## Tech stack

Python 3.10+, Django 5.2, Django REST Framework, Djoser, MySQL or SQLite

## Getting started

```bash
git clone https://github.com/syedakmall/little-lemon-capstone-project.git
cd little-lemon-capstone-project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata menu
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/restaurant/.

### Using MySQL

Install the driver and set the connection variables (see `.env.example`):

```bash
pip install mysqlclient
export MYSQL_DATABASE=littlelemon MYSQL_USER=littlelemon MYSQL_PASSWORD=secret
python manage.py migrate
```

If `MYSQL_DATABASE` is not set, the project uses a local `db.sqlite3` file.

### Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | development key | Set this in any deployed environment |
| `DJANGO_DEBUG` | `1` | Set to `0` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names |
| `MYSQL_*` | unset | MySQL connection settings |

## Website

| Path | Page |
| --- | --- |
| `/restaurant/` | Home |
| `/restaurant/about/` | About |
| `/restaurant/our-menu/` | Menu |
| `/restaurant/our-menu/<id>/` | Menu item |
| `/restaurant/book/` | Book a table |
| `/restaurant/reservations/` | Reservations (staff only) |
| `/admin/` | Django admin |

## API

All endpoints require an `Authorization: Token <token>` header, or a logged-in session.

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/auth/users/` | Register a user |
| POST | `/api-token-auth/` | Get a token (`username`, `password`) |
| POST | `/auth/token/login/` | Get a token through Djoser |
| GET, POST | `/restaurant/menu/` | List menu items, or create one (staff only) |
| GET, PUT, PATCH, DELETE | `/restaurant/menu/<id>/` | Retrieve or modify a menu item (writes are staff only) |
| GET, POST | `/restaurant/booking/tables/` | List or create bookings |
| GET, PUT, PATCH, DELETE | `/restaurant/booking/tables/<id>/` | Retrieve or modify a booking |

List endpoints accept `?search=` and `?ordering=`, for example `/restaurant/menu/?ordering=-price`.

### Example

```bash
curl -X POST http://127.0.0.1:8000/auth/users/ -d "username=demo&password=lemon-demo-2024"
curl -X POST http://127.0.0.1:8000/api-token-auth/ -d "username=demo&password=lemon-demo-2024"
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/restaurant/menu/
```

## Tests

```bash
python manage.py test
```

## Project structure

```
littlelemon/        project settings and root URLs
restaurant/
  fixtures/         sample menu data
  migrations/
  static/           CSS and images
  templates/        site templates
  tests/            model, API and page tests
  forms.py
  models.py
  permissions.py
  serializers.py
  urls.py
  views.py
```
