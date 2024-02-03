# -*- coding: utf-8 -*-
# pylint:disable=duplicate-code
from datetime import datetime

from omdb.exceptions.base import OmdbInvalidDataException
from omdb.models.movie import Movie, OmdbResultType, Rating, RatingQueryList


# pylint: disable=too-many-instance-attributes
class MovieCreateController:
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
        self,
        imdb_id: int,
        title: str = None,
        year: str = None,
        rated: str = None,
        released: datetime = None,
        runtime: str = None,
        genre: str = None,
        director: str = None,
        writer: str = None,
        actors: str = None,
        plot: str = None,
        language: str = None,
        country: str = None,
        awards: str = None,
        poster: str = None,
        metascore: int = None,
        imdb_rating: float = None,
        imdb_votes: str = None,
        dvd: str = None,
        box_office: str = None,
        production: str = None,
        website: str = None,
        ratings: list[dict] = None,
    ):
        self.imdb_id = imdb_id
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
        self.type = OmdbResultType.MOVIE
        self.dvd = dvd
        self.box_office = box_office
        self.production = production
        self.website = website
        self.ratings = ratings

        self.movie: Movie
        self._init_imdb_id()

    def _init_imdb_id(self):
        existing_movie = Movie.one_or_none(imdb_id=self.imdb_id)
        if existing_movie is not None:
            raise OmdbInvalidDataException('imdb_id')

    def run(self) -> Movie:
        self._create_movie()
        self._create_ratings()
        return self.movie

    def _create_movie(self):
        self.movie = Movie(
            title=self.title,
            year=self.year,
            rated=self.rated,
            released=self.released,
            runtime=self.runtime,
            genre=self.genre,
            director=self.director,
            writer=self.writer,
            actors=self.actors,
            plot=self.plot,
            language=self.language,
            country=self.country,
            awards=self.awards,
            poster=self.poster,
            metascore=self.metascore,
            imdb_rating=self.imdb_rating,
            imdb_votes=self.imdb_votes,
            imdb_id=self.imdb_id,
            type_=self.type,
            dvd=self.dvd,
            box_office=self.box_office,
            production=self.production,
            website=self.website,
            response=True,
        )
        self.movie.save()

    def _create_ratings(self):
        if not self.ratings:
            return

        movie_ratings = RatingQueryList()
        for rating in self.ratings:
            movie_rating = Rating(
                movie_id=self.movie.id,
                source=rating.get('source'),
                value=rating.get('value'),
            ).save()
            movie_ratings.append(movie_rating)

        self.movie.ratings = movie_ratings
        self.movie.save()
