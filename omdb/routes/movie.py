# -*- coding: utf-8 -*-
from flask import Blueprint

from omdb.config import config
from omdb.views.movie_multiple import movie_multiple

movies = Blueprint('movies', __name__, url_prefix=f'{config.API_PREFIX}/movies')


movies.add_url_rule('/', view_func=movie_multiple, methods=['GET'])

__all__ = ['movies']
