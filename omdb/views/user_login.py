# -*- coding: utf-8 -*-
from flask import Response, render_template

from omdb.controllers.user_login import UserLoginController
from omdb.exceptions.base import OmdbModelNotFoundException, OmdbUserException
from omdb.schema.user import UserSchema
from omdb.utils.form import LoginForm
from omdb.utils.http import error, success


def user_login() -> Response | str:
    form = LoginForm()
    if form.validate_on_submit():
        try:
            controller = UserLoginController(email=form.email.data, password=form.password.data)
            user = controller.run()
            return success(response_data=user, schema=UserSchema())
        except OmdbModelNotFoundException:
            return error(400, 'Invalid email')
        except OmdbUserException as e:
            return error(400, 'Invalid email or password', extra_keys={'exception': str(e)})

    return render_template('auth.html', form=form, text='Login', title='Login', btn_action='Login')
