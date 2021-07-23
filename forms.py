from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    ValidationError
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
    def check_letter(form, field):
        if not 'A' <= field.data <= 'I' and not 'a' <= field.data <= 'i':
            raise ValidationError('Field must be A - I')

    hectare_number = IntegerField('Hectare Number (01 - 42)',
                                  validators=[DataRequired(),
                                              NumberRange(1, 42,
                                                          'Must be 01 - 42')])
    hectare_letter = StringField('Hectare Letter (A - I)',
                                 validators=[DataRequired(),
                                             Length(min=1, max=1),
                                             check_letter])
    submit = SubmitField('Search')
