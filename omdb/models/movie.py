# -*- coding: utf-8 -*-
import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer

from omdb.db.base import StringColumn, TextColumn, UtcDateTimeColumn, db
from omdb.db.model import Model
from omdb.db.query import BaseQueryList


class OmdbResultType(enum.Enum):
    MOVIE = 'movie'
    SERIES = 'series'
    EPISODE = 'episode'


class RatingQueryList(BaseQueryList['Rating']):
    pass


class Rating(Model):
    __tablename__ = 'rating'
    querylist = RatingQueryList

    movie_id: int = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    source: str = StringColumn()
    value: str = StringColumn()

    def __init__(self, movie_id: int, source: str, value: str):
        super().__init__()
        self.movie_id = movie_id
        self.source = source
        self.value = value


class MovieQueryList(BaseQueryList['Movie']):
    pass


class Movie(Model):
    # pylint: disable=too-many-instance-attributes
    __tablename__ = 'movie'
    __repr_fields__ = ('imdb_id',)

    querylist = MovieQueryList

    title: str = StringColumn(index=True)
    year: str = StringColumn(max_length=4)
    rated: str = StringColumn()
    released: datetime = UtcDateTimeColumn(nullable=True)
    runtime: str = StringColumn()
    genre: str = StringColumn()
    director: str = StringColumn(max_length=1000)
    writer: str = StringColumn(max_length=1000)
    actors: str = StringColumn(max_length=1000)
    plot: str = TextColumn()
    language: str = StringColumn()
    country: str = StringColumn()
    awards: str = StringColumn(max_length=1000)
    poster: str = StringColumn(max_length=1000)
    metascore: int = Column(Integer)
    imdb_rating: float = Column(Float)
    imdb_votes: str = StringColumn()
    imdb_id: str = StringColumn(index=True, nullable=False)
    type: OmdbResultType = Column(Enum(OmdbResultType))
    dvd: str = StringColumn()
    box_office: str = StringColumn()
    production: str = StringColumn()
    website: str = StringColumn(max_length=1000)
    response: bool = Column(Boolean)
    ratings: RatingQueryList = db.relationship('Rating', backref='movie', cascade='all, delete-orphan')

    def __init__(
        # pylint: disable=too-many-arguments,too-many-locals
        self,
        title: str,
        year: str,
        rated: str,
        released: datetime,
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
        metascore: int,
        imdb_rating: float,
        imdb_votes: str,
        imdb_id: str,
        dvd: str,
        box_office: str,
        production: str,
        website: str,
        response: bool,
        type_: OmdbResultType = OmdbResultType.MOVIE,
    ):
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
