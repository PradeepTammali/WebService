# -*- coding: utf-8 -*-
from flask import Response
from flask_login import fresh_login_required

from omdb.controllers.user.user_delete import UserDeleteController
from omdb.exceptions.base import OmdbModelNotFoundException, OmdbUserException
from omdb.schema.user import UserSchema
from omdb.utils.http import error, success


@fresh_login_required
def user_delete(user_id: int) -> Response:
    try:
        controller = UserDeleteController(user_id=user_id)
        user = controller.run()
    except OmdbModelNotFoundException:
        return error(400, 'User not found')
    except OmdbUserException as e:
        return error(400, 'Invalid user', extra_keys={'exception': str(e)})

    return success(response_data=user, schema=UserSchema())
