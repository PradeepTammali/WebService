# -*- coding: utf-8 -*-
import secrets
from uuid import UUID, uuid4


def generate_request_id() -> str:
    # Will contain 36 characters.
    return str(UUID(bytes=secrets.token_bytes(16)))


def generate_email() -> str:
    return f'random-email-{uuid4()}@test.com'


def random_hash16() -> str:
    return secrets.token_hex(8)


def random_hash32() -> str:
    return secrets.token_hex(16)
