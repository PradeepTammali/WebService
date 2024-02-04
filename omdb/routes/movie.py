# -*- coding: utf-8 -*-
from flask import Blueprint

from omdb.config import config
from omdb.views.movie_create import movie_create
from omdb.views.movie_create_from_title import movie_create_from_title
from omdb.views.movie_delete import movie_delete
from omdb.views.movie_multiple import movie_multiple
from omdb.views.movie_one import movie_one

movies = Blueprint('movies', __name__, url_prefix=f'{config.API_PREFIX}/movies')


movies.add_url_rule('/', view_func=movie_create, methods=['POST'])
movies.add_url_rule('/', view_func=movie_multiple, methods=['GET'])
movies.add_url_rule('/<string:title>', view_func=movie_one, methods=['GET'])
movies.add_url_rule('/<string:title>', view_func=movie_create_from_title, methods=['POST'])
movies.add_url_rule('/<int:movie_id>', view_func=movie_delete, methods=['DELETE'])

__all__ = ['movies']
