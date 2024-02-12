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
