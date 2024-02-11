# -*- coding: utf-8 -*-
from flask_login import current_user

from omdb.exceptions.base import OmdbUserException
from omdb.models.user import User


class UserDeleteController:
    def __init__(self, user_id: int):
        self.user_id: int = user_id
        self.current_user: User = current_user
        self.user: User

        self._init_user()

    def _init_user(self):
        if not self.current_user.is_admin:
            raise OmdbUserException('current user is not admin')

        self.user = User.one(id=self.user_id)
        if self.user.id == self.current_user.id:
            raise OmdbUserException('operation not allowed on current user')

    def run(self) -> User:
        self._remove_user()
        return self.user

    def _remove_user(self):
        # TODO: logout the user and remove from session
        self.user.delete()
