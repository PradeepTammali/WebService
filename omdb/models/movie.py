# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import validates

from omdb.db.base import db
from omdb.db.model import Model


class Rating(Model):
    __tablename__ = 'rating'

    movie_id: int = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    source: str = Column(String)
    value: str = Column(String)

    @validates('movie_id')
    def validate_movie_id(self, key, movie_id) -> int:
        del key

        if not db.session.get(Movie, movie_id):
            raise ValueError(f'Movie with ID {movie_id} does not exist.')
        return movie_id

    def __init__(self, movie_id: int, source: str, value: str) -> None:
        super().__init__()
        self.movie_id = movie_id
        self.source = source
        self.value = value


class Movie(Model):
    # pylint: disable=too-many-instance-attributes
    __tablename__ = 'movie'

    title: str = Column(String, index=True)
    year: str = Column(String)
    rated: str = Column(String)
    released: str = Column(String)
    runtime: str = Column(String)
    genre: str = Column(String)
    director: str = Column(String)
    writer: str = Column(String)
    actors: str = Column(String)
    plot: str = Column(String)
    language: str = Column(String)
    country: str = Column(String)
    awards: str = Column(String)
    poster: str = Column(String)
    metascore: str = Column(String)
    imdb_rating: str = Column(String)
    imdb_votes: str = Column(String)
    imdb_id: str = Column(String, index=True)
    type: str = Column(String)
    dvd: str = Column(String)
    box_office: str = Column(String)
    production: str = Column(String)
    website: str = Column(String)
    response: str = Column(String)
    ratings: list[Rating] = db.relationship(
        'Rating', backref='movie', lazy=True, uselist=True, cascade='all, delete-orphan'
    )

    def __init__(
        # pylint: disable=too-many-arguments,too-many-locals
        self,
        title: str,
        year: str,
        rated: str,
        released: str,
        runtime: str,
        genre: str,
        director: str,
        writer: str,
        actors: str,
        plot: str,
        language: str,
        country: str,
        awards: str,
        poster: str,
        metascore: str,
        imdb_rating: str,
        imdb_votes: str,
        imdb_id: str,
        type_: str,
        dvd: str,
        box_office: str,
        production: str,
        website: str,
        response: str,
    ) -> None:
        super().__init__()
        self.title = title
        self.year = year
        self.rated = rated
        self.released = released
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writer = writer
        self.actors = actors
        self.plot = plot
        self.language = language
        self.country = country
        self.awards = awards
        self.poster = poster
        self.metascore = metascore
        self.imdb_rating = imdb_rating
        self.imdb_votes = imdb_votes
        self.imdb_id = imdb_id
        self.type = type_
        self.dvd = dvd
        self.box_office = box_office
        self.production = production
        self.website = website
        self.response = response
