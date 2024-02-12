# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])


class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    cpassword = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo('password', message='Passwords must match !'),
        ]
    )
