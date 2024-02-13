# -*- coding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Boolean, Column

from omdb.db.base import StringColumn
from omdb.db.model import Model
from omdb.login_manager import bcrypt


class User(Model, UserMixin):
    __tablename__ = 'user'
    __repr_fields__ = ('email',)

    email = StringColumn(unique=True, nullable=False)
    password = StringColumn(nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.is_admin = is_admin

    def get_id(self) -> str:
        return self.email
