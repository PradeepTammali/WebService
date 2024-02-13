# -*- coding: utf-8 -*-
from flask import Blueprint

from omdb.config import config
from omdb.views.user.user_delete import user_delete
from omdb.views.user.user_login import user_login
from omdb.views.user.user_logout import user_logout
from omdb.views.user.user_register import user_register

login = Blueprint('login', __name__, url_prefix=f'{config.API_PREFIX}/')

login.add_url_rule('/login', view_func=user_login, methods=['POST', 'GET'])
login.add_url_rule('/logout', view_func=user_logout, methods=['GET'])
login.add_url_rule('/register', view_func=user_register, methods=['POST', 'GET'])
login.add_url_rule('/delete/<int:user_id>', view_func=user_delete, methods=['DELETE'])

__all__ = ['login']
