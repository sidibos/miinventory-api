# Dockerized Django REST API

This is simple Django REST API build with Django REST Framework.
It is dockerized using docker-compose.
It uses PostgreSQL as database.

## Purpose

This project was a task for a job interview.
The purpose of this project is to demonstrate my skills in designing, building, documenting and testing REST API.
I chose to use Django REST Framework because it is a very popular framework for building REST APIs in Python and I
wanted to try it out. I selected PostgreSQL as the database because it is the most popular database for today's web
applications.

## Requirements

### Windows

Install Docker Desktop

### Linux and WSL2

- ``sudo apt install docker-compose``
- ``sudo service docker start``

## Installation

### Clone the repository

``git clone https://github.com/Jeb4dev/django-rest-api.git``

### Build and run the containers

``docker-compose up --build -d``

### Run the migrations

``docker-compose exec web python manage.py migrate``

#### Create a superuser - Optional

``docker-compose exec web python manage.py createsuperuser``

#### Run the tests - Optional

``docker-compose exec web python manage.py test``

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
