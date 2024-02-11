# -*- coding: utf-8 -*-
from flask import Response, render_template

from omdb.controllers.user_register import UserRegisterController
from omdb.exceptions.base import OmdbUserException
from omdb.schema.user import UserSchema
from omdb.utils.form import RegistrationForm
from omdb.utils.http import error, success


def user_register() -> Response | str:
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            controller = UserRegisterController(email=form.email.data, password=form.password.data)
            user = controller.run()
            return success(response_data=user, schema=UserSchema())
        except OmdbUserException as e:
            return error(400, 'Invalid email or password', extra_keys={'exception': str(e)})

    return render_template(
        'auth.html',
        form=form,
        text='Create account',
        title='Register',
        btn_action='Register account',
    )
