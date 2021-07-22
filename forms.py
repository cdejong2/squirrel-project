from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo
)


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    hectare_number = StringField('Hectare Number (01 - 42)',validators=[DataRequired()])
    hectare_letter = StringField('Hectare Letter (A - I)', validators=[DataRequired()])
    submit = SubmitField('Search')
