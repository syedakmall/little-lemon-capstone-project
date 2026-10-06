# Little Lemon Capstone Project

A Django and Django REST Framework back-end for Little Lemon, a Mediterranean restaurant in Chicago. Built for the Meta Back-End Developer capstone.

It includes a small website for guests, a REST API for the menu and table bookings, token authentication and a MySQL database.

## Setup

Create a MySQL database:

```sql
CREATE DATABASE littlelemon;
```

Install and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata menu
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/restaurant/.

The database connection defaults to `root` with no password on `127.0.0.1:3306`. To change it, set `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST` or `MYSQL_DATABASE` (see `.env.example`).

## API

Send `Authorization: Token <token>` with each request.

| Endpoint | Description |
| --- | --- |
| `POST /auth/users/` | Register |
| `POST /api-token-auth/` | Get a token |
| `/restaurant/menu/` | Menu items (only staff can add, edit or delete) |
| `/restaurant/menu/<id>/` | Single menu item |
| `/restaurant/booking/tables/` | Table bookings |
| `/restaurant/booking/tables/<id>/` | Single booking |

[Readme.txt](Readme.txt) has the full list of paths and example request bodies for testing in Insomnia.

## Tests

```bash
python manage.py test
```
