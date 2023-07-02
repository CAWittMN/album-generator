from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def generate_album_prompt(theme, genre, band):
    return f"generate a {theme} {genre} album from a fictional {theme} {genre} band named {band} with songs, song lengths in seconds, and {theme} album cover typical of {genre} bands"


def generate_band_prompt(theme, genre):
    return f"generate a {theme} {genre} band name with a {theme} biography about 400 characters long"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Columm(db.String, nullable=False)
    validated = db.Column(db.Boolean, default=False)

    liked_bands = db.relationship("Band", secondary="likes")

    bands = db.relationship("Band")

    @classmethod
    def register_user(cls, username, first_name, last_name, email, password):
        new_user = cls(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(password, user.password):
            return user
        return False


class Band(db.Model):
    __tablename__ = "bands"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres"))
    theme = db.Column(db.String, nullable=False)

    albums = db.relationship("Album")
    tags = db.relationship("Tag", secondary="tags_bands")

    @classmethod
    def register_band(cls, user_id, name, bio, genre_id, theme):
        new_band = cls(
            user_id=user_id, name=name, bio=bio, genre_id=genre_id, theme=theme
        )
        db.session.add(new_band)
        db.session.commit()


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)

    songs = db.relationship("Songs")

    @classmethod
    def register_album(cls, title, band, user):
        new_album = cls(title=title, band_id=band.id, user_id=user.id)

        db.session.add(new_album)
        db.session.commit()


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"))

    @classmethod
    def register_song(cls, title, duration_seconds, user, album, band):
        new_song = cls(
            title=title,
            duration_seconds=duration_seconds,
            user_id=user.id,
            album_id=album.id,
            band_id=band.id,
        )
        album.songs.append(new_song)
        db.session.commit()


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hypothetical = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String, nullable=False)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Tag_Band(db.Model):
    __tablename__ = "tags_bands"

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), primary_key=True)


class Like(db.Model):
    """Likes model"""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"))

    @classmethod
    def add_like(cls, user, band):
        new_like = cls(user_id=user.id, band_id=band.id)
        user.likes.append(new_like)
        db.session.commit()


def connect_to_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()
