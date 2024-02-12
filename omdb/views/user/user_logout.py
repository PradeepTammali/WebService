# -*- coding: utf-8 -*-
from flask import Response, redirect, url_for
from flask_login import login_required, logout_user

from omdb.utils.http import error


@login_required
def user_logout() -> Response:
    status = logout_user()
    if status is not True:
        return error(400, 'Can not logout')

    return redirect(url_for('login.user_login'))
