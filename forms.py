from wtforms import StringField, TextAreaField, PasswordField, EmailField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, ValidationError


def validate_name(form, field):
    if len(field.data.split()) != 2:
        raise ValidationError("Please enter only first and last name.")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired(), validate_name])
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
