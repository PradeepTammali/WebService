# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


class OmdbLoginManager(LoginManager):
    def __init__(self, app=None, add_context_processor=True):
        super().__init__(app, add_context_processor)
        # Session protection strong will prevent users from being access with token and also clears the token in reposense
        # Session protection basic will allow remember me functionality
        # Session protection None will allow user to be access with token
        self.session_protection = None
        self.login_message_category = 'info'
        self.login_view = 'login.user_login'


login_manager = OmdbLoginManager()
bcrypt = Bcrypt()
