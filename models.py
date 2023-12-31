from flask_sqlalchemy import SQLAlchemy, session
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt()

db = SQLAlchemy()


class User(db.Model):
    """User model with references to bands, albums, songs, and likes"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # validated = db.Column(db.Boolean, default=False)

    # liked_bands = db.relationship("Band", secondary="likes", backref="user_likes")

    bands = db.relationship("Band", backref="user", cascade="all, delete-orphan")
    albums = db.relationship("Album", backref="user", cascade="all, delete-orphan")
    songs = db.relationship("Song", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register_user(cls, username, first_name, last_name, email, password):
        """Register a new user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        new_user = cls(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user"""

        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

    @classmethod
    def make_name_dict(cls, name):
        """Takes a name and returns a dictionary with first and last name and formats capitalization"""
        name_dict = {}
        name_list = name.split()
        name_dict["first_name"] = name_list[0].capitalize()
        name_dict["last_name"] = name_list[1].capitalize()
        return name_dict


class Band(db.Model):
    """Band model with references to albums, songs, tags, and genre"""

    __tablename__ = "bands"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    theme = db.Column(db.String, nullable=False)
    prompt = db.Column(db.String, nullable=False, default="")
    photo = db.Column(db.String)  # nullable=False)

    genre = db.relationship("Genre", backref="bands")
    members = db.relationship("Member", backref="band", cascade="all, delete-orphan")
    albums = db.relationship("Album", backref="band", cascade="all, delete-orphan")
    songs = db.relationship("Song", backref="band", cascade="all, delete-orphan")
    # tags = db.relationship("Tag", secondary="tags_bands", backref="bands")

    @classmethod
    def register_band(cls, band_data, genre_id, user):
        """Register a new band"""

        new_band = cls(
            name=band_data["name"],
            bio=band_data["bio"],
            genre_id=genre_id,
            theme=band_data["theme"],
            photo=band_data["photo"],
            user_id=user.id,
            prompt=band_data["prompt"],
        )
        user.bands.append(new_band)
        db.session.add(new_band)
        db.session.commit()

        return new_band

    def to_dict(self):
        album_list = [album.to_dict() for album in self.albums]
        member_list = [member.to_dict() for member in self.members]
        # tag_list = [tag.name for tag in self.tags]

        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "members": member_list,
            "bio": self.bio,
            "genre": self.genre.name,
            "theme": self.theme,
            "photo": self.photo,
            "albums": album_list,
            # "tags": tag_list,
        }


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    @classmethod
    def make_member(cls, member, band_id):
        new_member = cls(name=member["name"], role=member["role"], band_id=band_id)
        return new_member

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
        }


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    artwork = db.Column(db.String, nullable=False)

    songs = db.relationship("Song", backref="album", cascade="all, delete-orphan")

    @classmethod
    def make_album(cls, album, band, user_id):
        """Register a new album"""
        new_album = cls(
            title=album["title"],
            artwork=album["albumArt"],
            band_id=band.id,
            user_id=user_id,
        )

        return new_album

    def to_dict(self):
        """Return a dictionary of the album data"""

        song_list = [song.to_dict() for song in self.songs]
        return {
            "id": self.id,
            "title": self.title,
            "songs": song_list,
            "artwork": self.artwork,
        }


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"))
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"))

    @classmethod
    def make_song(cls, song, user_id, album_id, band_id):
        """Register a new song"""
        new_song = cls(
            title=song["title"],
            duration_seconds=song["duration_seconds"],
            user_id=user_id,
            album_id=album_id,
            band_id=band_id,
        )
        return new_song

    def to_dict(self):
        """Return a dictionary of the song data"""

        return {
            "id": self.id,
            "title": self.title,
            "duration_seconds": self.duration_seconds,
        }


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    hypothetical = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "hypothetical": self.hypothetical,
            "description": self.description,
        }


# class Tag(db.Model):
#     __tablename__ = "tags"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)


# class Tag_Band(db.Model):
#     __tablename__ = "tags_bands"
#
#     tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
#     band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), primary_key=True)


# class Like(db.Model):
#     """Likes model"""
#
#     __tablename__ = "likes"
#
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     band_id = db.Column(db.Integer, db.ForeignKey("bands.id"))
#
#     @classmethod
#     def add_like(cls, user, band):
#         new_like = cls(user_id=user.id, band_id=band.id)
#         user.liked_bands.append(band)
#         db.session.add(new_like)
#         db.session.commit()


def connect_to_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
