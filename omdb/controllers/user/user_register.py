# -*- coding: utf-8 -*-
from omdb.exceptions.base import OmdbUserException
from omdb.models.user import User


class UserRegisterController:
    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password
        self.user: User

        self._init_user()

    def _init_user(self):
        user = User.one_or_none(email=self.email)
        if user:
            raise OmdbUserException('email already exists')

    def run(self) -> User:
        self._create_user()
        return self.user

    def _create_user(self):
        self.user = User(email=self.email, password=self.password)
        self.user.save()
