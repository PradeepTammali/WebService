# -*- coding: utf-8 -*-
import secrets
from uuid import uuid4


def generate_email() -> str:
    return f'random-email-{uuid4()}@test.com'


def generate_password() -> str:
    return secrets.token_hex(8)


def random_hash() -> str:
    return secrets.token_hex(16)
