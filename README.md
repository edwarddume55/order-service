# Order-service system

A Django REST API for managing customers and orders with SMS notifications.

## Features

- RESTful API for customers and orders
- OpenID Connect authentication usin Auth0
- SMS notifications via Africa's Talking
- Test coverage
- CI/CD pipeline

## Prerequisites

- Python 3.9+
- PostgreSQL

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Testing

Run tests with coverage:
```bash
pytest --cov=.
