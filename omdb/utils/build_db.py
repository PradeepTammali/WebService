# -*- coding: utf-8 -*-
import sys

from flask import Flask
from sqlalchemy_utils import database_exists, drop_database

from omdb.config import config
from omdb.db.base import db
from omdb.exceptions.base import OmdbInvalidDataException
from omdb.log import log
from omdb.models.movie import Movie, Rating
from omdb.models.user import User
from omdb.schema.build_db import MovieResultSchema, MovieSearchResultSchema
from omdb.utils.request import OmdbRequest

DATASET_SIZE = 100
omdb_api = OmdbRequest()


def _get_movie_imdb_ids() -> list[str]:
    _movie_imdb_ids = set()
    movies_results_schema = MovieSearchResultSchema()

    def _fetch_and_append_ids(page: int = 1) -> list[str]:
        _movies_results = omdb_api.search(page=page)
        movies_results = movies_results_schema.load(_movies_results)
        if movies_results['total_results'] < DATASET_SIZE:
            log.error('Insufficient data provided...')
            raise OmdbInvalidDataException(movies_results.get('total_results'))

        return [result.get('imdb_id') for result in movies_results['search']]

    _movie_imdb_ids.update(_fetch_and_append_ids())

    page = 2
    while len(_movie_imdb_ids) < DATASET_SIZE:
        _movie_imdb_ids.update(_fetch_and_append_ids(page=page))
        page += 1

    return list(_movie_imdb_ids)[:DATASET_SIZE]


def _get_movies_data(imdb_ids: list[str]) -> list[dict]:
    movies_data = []
    movie_schema = MovieResultSchema(exclude=('type',))
    for imdb_id in imdb_ids:
        _movie_data = omdb_api.get_by_imdb_id(imdb_id=imdb_id)
        movie_data = movie_schema.load(_movie_data)
        movies_data.append(movie_data)

    return movies_data


def _dump_data_to_db(movies_data: list[dict]):
    for movie_data in movies_data:
        ratings_data = []
        if 'ratings' in movie_data:
            ratings_data = movie_data.pop('ratings')
        movie = Movie(**movie_data)
        movie.save()
        if ratings_data:
            for rating_data in ratings_data:
                rating = Rating(movie_id=movie.id, **rating_data)
                rating.save()


def populate_data(app: Flask):
    if config.is_unittest():
        return

    with app.app_context():
        try:
            create_users()
            populate_database()
            db.session.commit()
        except Exception:  # pylint: disable=broad-exception-caught
            # Cleaning up database to build freshly
            db.session.rollback()
            db.drop_all()
            if database_exists(config.SQLALCHEMY_DATABASE_URI):
                drop_database(config.SQLALCHEMY_DATABASE_URI)
            log.error('Error while building database, Rerun the application to build database again...')
            sys.exit(1)

        log.info('Databae building successfull...')


def create_users():
    log.info('Creating default user...')
    if User.one_or_none(email=config.DEFAULT_USER_EMAIL) is not None:
        log.warning('Default user already exists, Skipping...')
        return

    User(email=config.DEFAULT_USER_EMAIL, password=config.DEFAULT_USER_PASSWORD, is_admin=True).save()
    log.info('Default user created...')


def populate_database():
    movies_count = Movie.count()
    if movies_count >= DATASET_SIZE:
        log.warning('Data exists in DB, skipping populating movies in database...')
        return

    log.info('Populating movies data in database...')
    movie_imdb_ids = _get_movie_imdb_ids()
    movies_data = _get_movies_data(imdb_ids=movie_imdb_ids)
    _dump_data_to_db(movies_data=movies_data)
    log.info('Movies databae building successfull...')
