# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


class OmdbLoginManager(LoginManager):
    def __init__(self, app=None, add_context_processor=True):
        super().__init__(app, add_context_processor)
        self.session_protection = 'strong'
        self.login_message_category = 'info'
        self.login_view = 'login.user_login'


login_manager = OmdbLoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id: int):
    # pylint: disable=import-outside-toplevel
    from omdb.models.user import User

    return User.one_or_none(id=user_id)
