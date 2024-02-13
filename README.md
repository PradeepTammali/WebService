# WebService

This document provides instructions on how to set up and run the application.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Docker
- Python 3.11.5
- Docker Compose
- Make (for development)

### Clone the Repository

To get a local copy of the code, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/PradeepTammali/WebService.git
cd WebService
```

## Usage

## Running as a Docker Service

```bash
docker compose up -d
```

The service will be accessible at [http://localhost:5555](http://localhost:5555)

## Running in a Local Environment

First, start the MySQL server:

```bash
docker compose up -d omdb-mysql
```

Then, run the application using one of the following commands:

`SERVICE_DATABASE_USER=root SERVICE_DATABASE_PASSWORD=1234 SERVICE_DATABASE_HOST=localhost SERVICE_DATABASE_PORT=3308 SERVICE_DATABASE_NAME=omdb gunicorn -b :5555 run:app`

or

`SERVICE_DATABASE_USER=root SERVICE_DATABASE_PASSWORD=1234 SERVICE_DATABASE_HOST=localhost SERVICE_DATABASE_PORT=3308 SERVICE_DATABASE_NAME=omdb FLASK_APP=run.py FLASK_RUN_PORT=5555 flask run`

The service will be accessible at [http://localhost:5555](http://localhost:5555)

### Development

Ensure `make` is installed on your system for development purposes.

To install and run the application, use:

`make all`

To run the application
`make run`

The service will be accessible at [http://localhost:5555](http://localhost:5555)

To run linting:
`make lint`

To run tests:
`make test`

## Description

Here's a summary of the endpoints:

Movie Endpoints (defined in `omdb/routes/movie.py`):

- `POST /movies/`: Creates a new movie. The logic is implemented in the `movie_create` function.
- `GET /movies/`: Retrieves multiple movies. The logic is implemented in the `movie_multiple` function.
- `GET /movies/<string:title>`: Retrieves a single movie by its title. The logic is implemented in the `movie_one` function.
- `POST /movies/<string:title>`: Creates a new movie from a title. The logic is implemented in the `movie_create_from_title` function.
- `DELETE /movies/<int:movie_id>`: Deletes a movie by its ID. The user must be verified to access this endpoint. The logic for deleting a movie is implemented in the `movie_delete` function.

Login Endpoints (defined in `omdb/routes/login.py`):

- `POST /login`: Logs in a user. The logic is implemented in the `user_login` function.
- `GET /login`: Retrieves login information. The logic is implemented in the `user_login` function.
- `GET /logout`: Logs out a user. The logic is implemented in the `user_logout` function.
- `POST /register`: Registers a new user. The logic is implemented in the `user_register` function.
- `GET /register`: Retrieves registration information. The logic is implemented in the `user_register` function.
- `GET /delete/<int:user_id>`: Deletes a user by its ID. The logic is implemented in the `user_delete` function.

Each of these endpoints is associated with a specific function in the views, which in turn uses a controller to interact with the data models. The controllers are defined in the `omdb/controllers/` directory.
