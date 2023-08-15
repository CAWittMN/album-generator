import os
import json
import openai
from flask_debugtoolbar import DebugToolbarExtension
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session,
    g,
    flash,
    request,
    jsonify,
)
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from models import (
    connect_to_db,
    db,
    bcrypt,
    User,
    Band,
    Album,
    Song,
    # Like,
    Member,
    Genre,
    # Tag,
)
from forms import LoginForm, UserForm, NewPasswordForm, GenerateForm

# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.Model.list()

CURR_USER_KEY = "curr_user"
SALT = os.environ.get("SALT", "tempkey")

app = Flask(__name__)
# mail = Mail(app)
# serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "tempkey"))

# app.config["MAIL_SERVER"] = "smtp.mail.com"
# app.config["MAIL_PORT"] = 465
# app.config["MAIL_USE_SSL"] = True
# app.config["MAIL_USE_TLS"] = False
# app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "tempname")
# app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "temppassword")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tempkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///album_generator"
)
toolbar = DebugToolbarExtension(app)


connect_to_db(app)

test_band = """{
    "name": "The Beatles",
    "bio": "The Beatles were an English rock band formed in Liverpool in 1960. The group, whose best-known line-up comprised John Lennon, Paul McCartney, George Harrison and Ringo Starr, are regarded as the most influential band of all time. They were integral to the development of 1960s counterculture and popular music's recognition as an art form. Rooted in skiffle, beat and 1950s rock and roll, their sound incorporated elements of classical music and traditional pop in innovative ways; the band later explored music styles ranging from ballads and Indian music to psychedelia and hard rock. As pioneers in recording, songwriting and artistic presentation, the group revolutionised many aspects of the music industry and were often publicised as leaders of the era's youth and sociocultural movements.",
    "members": [
        {
            "name": "John Lennon",
            "role": "guitar"
        },
        {
            "name": "Paul McCartney",
            "role": "bass"
        },
        {
            "name": "George Harrison",
            "role": "guitar"
        }, 
        {
            "name": "Ringo Starr",
            "role": "drums"
        }
    ],
    "albums": [ 
        {
            "title": "Abbey Road",
            "songs": [
                {
                    "title": "Come Together",
                    "duration_seconds": 259
                },
                {
                    "title": "Something",
                    "duration_seconds": 182
                },
                {
                    "title": "Maxwell's Silver Hammer",
                    "duration_seconds": 203
                },
                {
                    "title": "Oh! Darling",
                    "duration_seconds": 210
                },
                {
                    "title": "Octopus's Garden",
                    "duration_seconds": 177
                },
                {
                    "title": "I Want You (She's So Heavy)",
                    "duration_seconds": 467
                },
                {
                    "title": "Here Comes the Sun",
                    "duration_seconds": 185
                },
                {
                    "title": "Because",
                    "duration_seconds": 163
                },
                {
                    "title": "You Never Give Me Your Money",
                    "duration_seconds": 252
                },
                {
                    "title": "Sun King",
                    "duration_seconds": 156
                },
                {
                    "title": "Mean Mr. Mustard",
                    "duration_seconds": 86
                },
                {
                    "title": "Polythene Pam",
                    "duration_seconds": 83
                },
                {
                    "title": "She Came in Through the Bathroom Window",
                    "duration_seconds": 129
                },
                {
                    "title": "Golden Slumbers",
                    "duration_seconds": 91
                },
                {
                    "title": "Carry That Weight",
                    "duration_seconds": 90
                },
                {
                    "title": "The End",
                    "duration_seconds": 124
                },
                {
                    "title": "Her Majesty",
                    "duration_seconds": 23
                }
            ]
        }
    ]
}"""


@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


#########################################################################################
# Homepage Routes


@app.route("/")
def show_homepage():
    if g.user:
        return redirect(url_for("logged_in_home"))
    form = LoginForm()
    bands = Band.query.order_by(func.random()).limit(30).all()

    return render_template("home.html", form=form, bands=bands)


#########################################################################################
# Login/Logout/Signup Routes


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    if g.user:
        return redirect(url_for("logged_in_home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            # if user.validated == False:
            #    return redirect(url_for("validate_email", user_id=user.id))
            return redirect(url_for("logged_in_home"))

        flash("Invalid credentials.")
        return redirect(url_for("show_homepage"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Logged out.", "alert-success")
    return redirect(url_for("show_homepage"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    if g.user:
        return redirect(url_for("logged_in_home"))

    form = UserForm()

    if form.validate_on_submit():
        name = User.make_name_dict(form.name.data)
        try:
            user = User.register_user(
                username=form.username.data,
                first_name=name["first_name"],
                last_name=name["last_name"],
                email=form.email.data,
                password=form.password.data,
            )
        except IntegrityError:
            flash("Username already taken.")
            return redirect(url_for("signup"))

        do_login(user)
        # return redirect(url_for('send_validation_email'))
        return redirect(url_for("logged_in_home"))

    return render_template("signup.html", form=form)


#########################################################################################
# Email Validation Routes


# @app.route("/validate", methods=["GET"])
# def send_validation_email():
#     """Send validation email"""
#
#     if g.user == None:
#         return redirect(url_for("home"))
#
#     if g.user.validated == True:
#         flash("Your email is already validated!")
#         return redirect(url_for("logged_in_home"))
#
#     token = serializer.dumps(g.user.email, salt=SALT)
#     msg = Message(
#         "Confirm Email",
#         sender="NoReply@album-band-generator.com",
#         recipients=[g.user.email],
#     )
#     link = url_for("validate_email", user_id=g.user.id, token=token, _external=True)
#     msg.body = "Your validation link is {} and will expire in 3 hours.".format(link)
#     mail.send(msg)
#
#     return render_template("validate_email.html")
#
#
# @app.route("/validate/<int:user_id>/<token>")
# def validate_email(user_id, token):
#     """Validate user email"""
#
#     user = User.query.get_or_404(user_id)
#
#     if user.validated == True:
#         return redirect(url_for("show_homepage"))
#
#     try:
#         email = serializer.loads(token, salt=SALT, max_age=10800)
#     except SignatureExpired:
#         flash("The token is expired, please request a new one.")
#         return url_for("resend_validation", user_id=user_id)
#
#     except BadTimeSignature:
#         flash("The token is invalid. Please request a new one and try again.")
#         return url_for("resend_validation", user_id=user_id)
#
#     if user.email == email:
#         user.validated = True
#         db.session.commit()
#         do_login(user)
#         flash("Your email has been validated!")
#         return redirect(url_for("logged_in_home"))
#
#
# @app.route("/resend_validation/<int:user_id>", methods=["GET"])
# def resend_validation(user_id):
#     """Resend validation email"""
#
#     user = User.query.get_or_404(user_id)
#     if user.validated == True:
#         return redirect(url_for("show_homepage"))
#
#     return render_template("resend_validation.html", user=user)


#########################################################################################
# User Routes


@app.route("/user_home")
def logged_in_home():
    if not g.user:
        return redirect(url_for("show_homepage"))
    # if g.user.validated == False:
    #    flash("Please validate your email to continue.")
    #    return redirect(url_for("resend_validation", user_id=g.user.id))
    #
    form = GenerateForm()
    form.genre.choices = [(genre.name, genre.name) for genre in Genre.query.all()]
    return render_template("logged_in_home.html", form=form, user=g.user)


# def show_user(user_id):
# @app.route("/users/<int:user_id>")
#     """Show user details"""
#
#     if g.user.id == user_id:
#         return redirect(url_for("logged_in_home"))
#
#     user = User.query.get_or_404(user_id)
#     return render_template("user.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    if g.user.id != user_id:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.")
    return redirect(url_for("show_homepage"))


@app.route("/users/edit", methods=["GET", "POST"])
def edit_user():
    """Edit user"""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))

    form = UserForm(obj=g.user)

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data) == False:
            flash("Incorrect password.")
            return redirect(url_for("edit_user"))

        name = User.make_name_dict(form.name.data)
        g.user.first_name = name["first_name"]
        g.user.last_name = name["last_name"]
        g.user.email = form.email.data
        db.session.commit()
        flash("User updated.")
        return redirect(url_for("logged_in_home"))

    return render_template("edit_user.html", user=g.user, form=form)


@app.route("/users/edit/password", methods=["GET", "POST"])
def edit_password():
    """Edit user password"""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))

    form = NewPasswordForm()

    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.old_password.data) == False:
            flash("Incorrect password.")
            return redirect(url_for("edit_password"))

        new_hashed_pwd = bcrypt.generate_password_hash(form.new_password.data).decode(
            "UTF-8"
        )
        g.user.password = new_hashed_pwd
        db.session.commit()
        flash("Password updated.")
        return redirect(url_for("logged_in_home"))
    return render_template("edit_password.html", form=form)


#########################################################################################
# Band Routes


@app.route("/bands/<int:band_id>")
def show_band(band_id):
    """Show band details"""

    band = Band.query.get_or_404(band_id)
    return render_template("band.html", band=band)


# @app.route("/api/bands/<int:band_id>/like/<int:user_id>", methods=["POST"])
# def add_remove_like_band(band_id, user_id):
#     """Like a band"""
#
#     user = User.query.get(user_id)
#     band = Band.query.get(band_id)
#     if band in user.liked_bands:
#         user.liked_bands.remove(band)
#     else:
#         user.liked_bands.append(band)
#     db.session.commit()
#     return jsonify({"success": True})


@app.route("/bands/<int:band_id>./delete", methods=["POST"])
def delete_band(band_id):
    """Delete band"""

    band = Band.query.get_or_404(band_id)
    if g.user.id != band.user_id:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))
    db.session.delete(band)
    db.session.commit()
    flash("Band deleted.")
    return redirect(url_for("logged_in_home"))


@app.route("/albums/<int:album_id>./delete", methods=["POST"])
def delete_album(album_id):
    """Delete album"""

    album = Album.query.get_or_404(album_id)
    if g.user.id != album.user_id:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))
    db.session.delete(album)
    db.session.commit()
    flash("Album deleted.")
    return redirect(url_for("show_band", band_id=album.band_id))


#########################################################################################
# API Routes


###########################
# OpenAI API Routes


def generate_band_prompt(theme, genre, add_prompt):
    """Generate a prompt for a band"""

    prompt = [
        {
            "role": "system",
            "content": f"You are a data generating bot and will generate data for a {theme} reflection of a band with a name, short biography origin story, members, an album, and songs for that album. The data you generate will be a {theme} reflection of the genre and the data will be in json format. You will format the data like so: {{name:, bio:, members: [{{name:, role:}}], albums: [{{title:, songs: [{{title:, duration_seconds:}}]}}]}}",
        },
        {
            "role": "user",
            "content": f"Generate a {genre} band. {add_prompt}",
        },
    ]

    return prompt


def generate_band_img_prompt(theme, genre, members_num, add_prompt):
    """Generate a prompt for a band image"""
    prompt = f"A {theme}, studio photographic, group photo of a {genre} band with {members_num} members. {add_prompt}"
    return prompt


def generate_album_artwork_prompt(theme, genre, band_name, album_name, add_prompt):
    """Generate a prompt for an album artwork"""

    prompt = f"Album art for a {genre} band named '{band_name}'. The album name is {album_name} and has an obvious {theme} theme. {add_prompt}"
    return prompt


@app.route("/api/generate/band-data/<theme>/<genre>/<add_prompt>", methods=["GET"])
def generate_band_data_api(theme, genre, add_prompt):
    """Generate a new band"""
    prompt = generate_band_prompt(theme=theme, genre=genre, add_prompt=add_prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
    text = response["choices"][0].message.content.strip()
    print(text)
    data = json.loads(text)
    # data = json.loads(test_band.strip())
    return jsonify(data=data)


@app.route(
    "/api/generate/img/<theme>/<genre>/<int:members_num>/<add_prompt>", methods=["GET"]
)
def generate_band_img_api(theme, genre, members_num, add_prompt):
    """Generate a band image"""
    prompt = generate_band_img_prompt(
        theme=theme, genre=genre, members_num=members_num, add_prompt=add_prompt
    )
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
    )
    print(response)
    url = response["data"][0]["url"]
    # url = "test.com"
    return jsonify(url=url)


@app.route(
    "/api/generate/album-art/<theme>/<genre>/<band_name>/<album_name>/<add_prompt>",
    methods=["GET"],
)
def generate_album_artwork_api(theme, genre, band_name, album_name, add_prompt):
    """Generate an album artwork"""
    prompt = generate_album_artwork_prompt(
        theme=theme,
        genre=genre,
        band_name=band_name,
        album_name=album_name,
        add_prompt=add_prompt,
    )
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
    )
    print(response)
    url = response["data"][0]["url"]
    # url = "test.com"
    return jsonify(url=url)


###########################
# RESTful API Routes


@app.route("/api/band", methods=["POST"])
def post_band():
    """Create a new band"""
    band_data = request.json
    user = User.query.get_or_404(g.user.id)
    genre = Genre.query.filter_by(name=band_data["genre"]).first()
    # tags_list = data["tags"]
    # tags = Tag.query.filter(Tag.name.in_(tags_list)).all()
    band = Band.register_band(band_data=band_data, genre=genre, user=user)
    for member in band_data["members"]:
        new_member = Member.make_member(member=member, band_id=band.id)
        band.members.append(new_member)

    album = Album.make_album(band=band, album=band_data["albums"][0], user_id=g.user.id)
    for song in band_data["albums"][0]["songs"]:
        new_song = Song.make_song(
            song=song, album_id=album.id, user_id=g.user.id, band_id=band.id
        )
        album.songs.append(new_song)
    band.albums.append(album)
    db.session.commit()
    return jsonify(band=band.to_dict())


@app.route("/api/bands")
def get_bands():
    """Return list of all bands."""

    bands = [band.to_dict() for band in Band.query.order_by(Band.name.desc()).all()]

    return jsonify(bands=bands)


@app.route("/api/bands/<int:band_id>")
def get_band(band_id):
    """Return a band by id."""

    band = Band.query.get_or_404(band_id)

    return jsonify(band=band.to_dict())


# @app.route("/api/bands/name/<string:name>")
# def get_bands_by_like_name(name):
#    """Return a list of bands by name"""
#
#    bands = [
#        band.to_dict() for band in Band.query.filter(Band.name.ilike(f"%{name}%")).all()
#    ]
#
#    return jsonify(bands=bands)


# @app.route("/api/bands/tags/")
# def get_bands_by_tags():
#     """Return a list of bands by tags"""
#
#     tags = request.args.getlist("tags")
#     bands = [
#         band.to_dict()
#         for band in Band.query.filter(Band.tags.any(Tag.name.in_(tags))).all()
#     ]


# @app.route("/api/bands/genre/<int:genre_id>")
# def get_bands_by_genre(genre_id):
#    """Return a list of bands by genre id."""
#
#    bands = [band.to_dict() for band in Band.query.filter_by(genre_id=genre_id).all()]
#
#    return jsonify(bands=bands)


# @app.route("/api/bands/theme/<string:theme>")
# def get_bands_by_theme(theme):
#    """Return a list of bands by theme."""
#
#    bands = [band.to_dict() for band in Band.query.filter_by(theme=theme).all()]
#
#    return jsonify(bands=bands)


# @app.route("/api/bands/genre/<int:genre_id>/theme/<string:theme>")
# def get_bands_by_genre_and_theme(genre_id, theme):
#    """Return a list of bands by genre id and theme."""
#
#    bands = [
#        band.to_dict()
#        for band in Band.query.filter_by(genre_id=genre_id, theme=theme).all()
#    ]
#
#    return jsonify(bands=bands)


# @app.route("/api/bands/genre/<int:genre_id>/theme/<string:theme>/tags")
# def get_bands_by_genre_theme_and_tags(genre_id, theme):
#     """Return a list of bands by genre id and theme."""
#
#     tags = request.args.getlist("tags")
#     bands = [
#         band.to_dict()
#         for band in Band.query.filter_by(genre_id=genre_id, theme=theme)
#         .filter(Band.tags.any(Tag.name.in_(tags)))
#         .all()
#     ]
#
#     return jsonify(bands=bands)


@app.route("/api/genre/<genre_name>")
def get_genre(genre_name):
    """Return a genre by name."""
    genre = Genre.query.filter_by(name=genre_name).first()
    return jsonify(genre=genre.to_dict())
