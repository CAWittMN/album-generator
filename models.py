from flask_sqlalchemy import SQLAlchemy, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()


def generate_prompt(theme, genre):
    """Generate a prompt for the user to use in the API call"""
    return f"generate a {genre} band name with a {theme} biography about 400 characters long, a {theme} album title with {theme} songs and song lengths, and a {theme} album cover typical of {genre} bands. Format the response in json."


class User(db.Model):
    """User model with references to bands, albums, songs, and likes"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    validated = db.Column(db.Boolean, default=False)

    liked_bands = db.relationship("Band", secondary="likes", backref="user_likes")

    bands = db.relationship("Band", backref="user")
    albums = db.relationship("Album", backref="user")
    songs = db.relationship("Song", backref="user")

    @classmethod
    def register_user(cls, username, first_name, last_name, email, password):
        """Register a new user"""

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
        """Authenticate a user"""

        user = cls.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(password, user.password):
            return user
        return False

    @classmethod
    def make_name_dict(name):
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
    genre = db.Column(db.Integer, db.ForeignKey("genres.name"))
    theme = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String, nullable=False)

    members = db.relationship("Member", backref="band")
    genre = db.relationship("Genre", backref="bands")
    albums = db.relationship("Album", backref="band")
    songs = db.relationship("Song", backref="band")
    tags = db.relationship("Tag", secondary="tags_bands", backref="bands")

    @classmethod
    def register_band(cls, user, name, bio, genre_id, theme):
        new_band = cls(
            user_id=user.id, name=name, bio=bio, genre_id=genre_id, theme=theme
        )
        user.bands.append(new_band)
        db.session.add(new_band)
        db.session.commit()

    def to_dict(self):
        album_list = [album.to_dict() for album in self.albums]
        member_list = [member.to_dict() for member in self.members]
        tag_list = [tag.name for tag in self.tags]

        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "members": member_list,
            "bio": self.bio,
            "genre": self.genre.name,
            "theme": self.theme,
            "photo_url": self.photo_url,
            "albums": album_list,
            "tags": tag_list,
        }


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey("bands.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    @classmethod
    def register_member(cls, name, role, band):
        new_member = cls(name=name, role=role, band_id=band.id)
        band.members.append(new_member)
        db.session.add(new_member)
        db.session.commit()

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
    artwork_url = db.Column(db.String, nullable=False)

    songs = db.relationship("Songs", backref="album")

    @classmethod
    def register_album(cls, title, band, user):
        """Register a new album"""

        new_album = cls(title=title, band_id=band.id, user_id=user.id)
        user.albums.append(new_album)
        band.albums.append(new_album)
        db.session.add(new_album)
        db.session.commit()

    def to_dict(self):
        """Return a dictionary of the album data"""

        song_list = [song.to_dict() for song in self.songs]
        return {
            "id": self.id,
            "title": self.title,
            "songs": song_list,
            "artwork": self.artwork_url,
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
    def register_song(cls, songs, user, album, band):
        """Register a new song"""
        for song in songs:
            new_song = cls(
                user_id=user.id,
                album_id=album.id,
                band_id=band.id,
                title=song["title"],
                duration_seconds=song["duration_seconds"],
            )
            user.songs.append(new_song)
            band.songs.append(new_song)
            album.songs.append(new_song)
            db.session.add(new_song)
            db.session.commit()

        def to_dict(self):
            """Return a dictionary of the song data"""

            return {
                "id": self.id,
                "title": self.title,
                "duration_seonds": self.duration_seconds,
            }


class Genre(db.Model):
    __tablename__ = "genres"

    name = db.Column(db.String, primary_key=True, nullable=False, unique=True)
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
        user.liked_bands.append(band)
        db.session.add(new_like)
        db.session.commit()


def connect_to_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()
