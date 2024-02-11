# -*- coding: utf-8 -*-
from flask_bcrypt import check_password_hash
from flask_login import login_user

from omdb.exceptions.base import OmdbUserException
from omdb.models.user import User


class UserLoginController:
    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password
        self.user: User

        self._init_user()

    def _init_user(self):
        self.user = User.one(email=self.email)

    def run(self) -> User:
        self._verify_password()
        self._login_user()
        return self.user

    def _verify_password(self):
        if not check_password_hash(self.user.password, self.password):
            raise OmdbUserException('password')

    def _login_user(self):
        status = login_user(self.user)
        if status is not True:
            raise OmdbUserException('user')
