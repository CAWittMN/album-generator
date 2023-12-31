from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    EmailField,
    SelectField,
    IntegerField,
    FieldList,
    FormField,
)
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


class GenerateForm(FlaskForm):
    theme = StringField("Theme", validators=[InputRequired()])
    genre = SelectField("Genre", validators=[InputRequired()])
    additional_prompt = TextAreaField("Additional details")


class NewPasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[InputRequired()])
    new_password = PasswordField("New password", validators=[InputRequired()])
