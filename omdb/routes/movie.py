# -*- coding: utf-8 -*-
from flask import Blueprint

from omdb.config import config
from omdb.views.movie_create import movie_create
from omdb.views.movie_multiple import movie_multiple
from omdb.views.movie_one import movie_one

movies = Blueprint('movies', __name__, url_prefix=f'{config.API_PREFIX}/movies')


movies.add_url_rule('/', view_func=movie_create, methods=['POST'])
movies.add_url_rule('/', view_func=movie_multiple, methods=['GET'])
movies.add_url_rule('/<string:title>', view_func=movie_one, methods=['GET'])

__all__ = ['movies']
