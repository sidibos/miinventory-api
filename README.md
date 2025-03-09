# Miinventory API

This is the API for miinventory web build with Django REST Framework.
It is dockerized using docker-compose.
It uses PostgreSQL as database.

## Purpose

This API will be consumed by miinventory web built in React

## Requirements

### Windows

- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Linux and WSL2

- ``sudo apt install docker-compose``
- ``sudo service docker start``

## Installation

You can either host the application with docker (recommended) or locally without docker.

### Clone the repository

``git clone https://github.com/Jeb4dev/django-rest-api.git``

### Host with docker

#### Build and run the containers

``docker-compose up --build -d``

#### Run the migrations

``docker-compose exec web python manage.py migrate``

#### Create a superuser - Optional

``docker-compose exec web python manage.py createsuperuser``

#### Run the tests - Optional

``docker-compose exec web python manage.py test``

### Host locally without docker - Not Recommended

If you want to host the application locally without docker, you will need to have Python 3.10+ installed.
After than run the following commands:

````
cd .\app\
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

---

## Development

### Migration

If you make changes to the models, you will need to create migrations and run them to update the database.

``docker-compose exec web python manage.py makemigrations``
``docker-compose exec web python manage.py migrate``

### Running without Docker

#### Install the requirements

``pip install -r requirements.txt`` found in /app directory.

Set up the environment variables in ``dev.env`` file

#### Run the server

``python manage.py runserver``

### Application Folder Structure

````bash
app/
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── django-rest-api/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── Dockerfile
├── manage.py
└── requirements.txt
````

#### Project

- `api/`: This directory contain the files for the API Django app:
  - `migrations`/: This directory contains database migration files.
    - `0001_initial.py`: Contains the initial migration for database.
  - `models.py`: Defines Django models, in this case User object.
  - `serializers.py`: Defines how Django models, in this case "User" should be serialized into JSON.
  - `tests.py`: Contains API tests.
  - `urls.py`: Defines API endpoint URL's.
  - `views.py`: Contains API endpoints functions.
- `django-rest-api/`: Part of Django’s configuration. Acts as "core" for the Django project.
  - `asgi.py:` Part of Django’s configuration.
  - `settings.py`: Contains your project’s settings.
  - `urls.py:` Defines available URL's.
  - `wsgi.py:` Part of Django’s configuration.
- `Dockerfile`: Builds a Docker image for containerization.
- `manage.py`: This is a command-line utility for example running the server, create database tables, etc.
- `requirements.txt`: List all project dependencies.

## API Documentation

The API documentation is available at [localhost:8000](http://localhost:8000/). It is generated using
[Swagger](https://swagger.io/). You need to start the server in order to see the documentation as it is being hosted
locally.

## License

This project is licensed under the MIT License.
