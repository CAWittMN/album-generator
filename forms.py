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


class MemberForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    role = StringField("Role", validators=[InputRequired()])


class SongForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    duration_seconds = IntegerField("Duration in seconds", validators=[InputRequired()])


class AlbumForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    songs = FieldList(FormField(SongForm), min_entries=1, max_entries=20)


class BandForm(FlaskForm):
    name = StringField("Band name", validators=[InputRequired()])
    bio = TextAreaField("Bio", validators=[InputRequired()])
    members = FieldList(FormField(MemberForm), min_entries=1, max_entries=15)
    album = FormField(AlbumForm)


class NewPasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[InputRequired()])
    new_password = PasswordField("New password", validators=[InputRequired()])
