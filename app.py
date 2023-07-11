import os
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
from models import (
    connect_to_db,
    db,
    generate_prompt,
    bcrypt,
    User,
    Band,
    Album,
    Song,
    Like,
    Genre,
    Tag,
)
from forms import LoginForm, UserForm, BandForm, NewPasswordForm
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.Model.list()

CURR_USER_KEY = "curr_user"
SALT = os.environ.get("SALT", "tempkey")

app = Flask(__name__)
mail = Mail(app)
serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "tempkey"))

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tempkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///album_generator"
)
toolbar = DebugToolbarExtension(app)


connect_to_db(app)

#########################################################################################
# Homepage Routes


@app.route("/")
def show_homepage():
    if g.user:
        return redirect(url_for("logged_in_home"))
    form = LoginForm()
    bands = Band.query.order_by(func.random()).limit(30).all()

    return render_template("home.html", form=form)


#########################################################################################
# Login/Logout/Signup Routes


@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


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
            if user.validated == False:
                return redirect(url_for("validate_email", user_id=user.id))
            return redirect(url_for("logged_in_home"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Logged out.")
    return redirect(url_for("show_homepage"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    if g.user:
        return redirect(url_for("logged_in_home"))

    form = UserForm()

    if form.validate_on_submit():
        name = User.make_name_dict(form.name.data)
        user = User.register_user(
            username=form.username.data,
            first_name=name["first_name"],
            last_name=name["last_name"],
            email=form.email.data,
            password=form.password.data,
        )
        do_login(user)
        return redirect(url_for("validate_email"))

    return render_template("signup.html", form=form)


#########################################################################################
# Email Validation Routes


@app.route("/validate", methods=["GET"])
def send_validation_email():
    """Send validation email"""

    if g.user == None:
        return redirect(url_for("home"))

    if g.user.validated == True:
        flash("Your email is already validated!")
        return redirect(url_for("logged_in_home"))

    token = serializer.dumps(g.user.email, salt=SALT)
    msg = Message(
        "Confirm Email",
        sender="NoReply@album-band-generator.com",
        recipients=[g.user.email],
    )
    link = url_for("validate_email", user_id=g.user.id, token=token, _external=True)
    msg.body = "Your validation link is {} and will expire in 3 hours.".format(link)
    mail.send(msg)

    return render_template("validate_email.html")


@app.route("/validate/<int:user_id>/<token>")
def validate_email(user_id, token):
    """Validate user email"""

    user = User.query.get_or_404(user_id)

    if user.validated == True:
        return redirect(url_for("show_homepage"))

    try:
        email = serializer.loads(token, salt=SALT, max_age=10800)
    except SignatureExpired:
        flash("The token is expired, please request a new one.")
        return url_for("resend_validation", user_id=user_id)

    except BadTimeSignature:
        flash("The token is invalid. Please request a new one and try again.")
        return url_for("resend_validation", user_id=user_id)

    if user.email == email:
        user.validated = True
        db.session.commit()
        do_login(user)
        flash("Your email has been validated!")
        return redirect(url_for("logged_in_home"))


@app.route("/resend_validation/<int:user_id>", methods=["GET"])
def resend_validation(user_id):
    """Resend validation email"""

    user = User.query.get_or_404(user_id)
    if user.validated == True:
        return redirect(url_for("show_homepage"))

    return render_template("resend_validation.html", user=user)


#########################################################################################
# User Routes


@app.route("/user_home")
def logged_in_home():
    if not g.user:
        return redirect(url_for("show_homepage"))
    if g.user.validated == False:
        flash("Please validate your email to continue.")
        return redirect(url_for("resend_validation", user_id=g.user.id))

    return render_template("logged_in_home.html", user=g.user)


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user details"""

    if g.user.id == user_id:
        return redirect(url_for("logged_in_home"))

    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


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


@app.route("/api/bands/<int:band_id>/like/<int:user_id", methods=["POST"])
def add_remove_like_band(band_id, user_id):
    """Like a band"""

    user = User.query.get(user_id)
    band = Band.query.get(band_id)
    if band in user.liked_bands:
        user.liked_bands.remove(band)
    else:
        user.liked_bands.append(band)
    db.session.commit()
    return jsonify({"success": True})


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


@app.route("bands/new", methods=["GET", "POST"])
def create_band():
    """Create a new band"""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(url_for("show_homepage"))

    form = BandForm()

    if form.validate_on_submit():
        # use openai api here
        # prompt = generate_prompt(form.theme.data, form.genre.data)

        flash("Band created.")
        return redirect(url_for("logged_in_home"))

    return render_template("new_band.html", form=form)


#########################################################################################
# API Routes


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


@app.route("/api/bands/name/<string:name>")
def get_bands_by_like_name(name):
    """Return a list of bands by name"""

    bands = [
        band.to_dict() for band in Band.query.filter(Band.name.ilike(f"%{name}%")).all()
    ]

    return jsonify(bands=bands)


# get band by tags
@app.route("/api/bands/tags/")
def get_bands_by_tags():
    """Return a list of bands by tags"""

    tags = request.args.getlist("tags")
    bands = [
        band.to_dict()
        for band in Band.query.filter(Band.tags.any(Tag.name.in_(tags))).all()
    ]


@app.route("/api/bands/genre/<int:genre_id>")
def get_bands_by_genre(genre_id):
    """Return a list of bands by genre id."""

    bands = [band.to_dict() for band in Band.query.filter_by(genre_id=genre_id).all()]

    return jsonify(bands=bands)


@app.route("/api/bands/theme/<string:theme>")
def get_bands_by_theme(theme):
    """Return a list of bands by theme."""

    bands = [band.to_dict() for band in Band.query.filter_by(theme=theme).all()]

    return jsonify(bands=bands)


@app.route("/api/bands/genre/<int:genre_id>/theme/<string:theme>")
def get_bands_by_genre_and_theme(genre_id, theme):
    """Return a list of bands by genre id and theme."""

    bands = [
        band.to_dict()
        for band in Band.query.filter_by(genre_id=genre_id, theme=theme).all()
    ]

    return jsonify(bands=bands)


@app.route("/api/bands/genre/<int:genre_id>/theme/<string:theme>/tags/")
def get_bands_by_genre_theme_and_tags(genre_id, theme):
    """Return a list of bands by genre id and theme."""

    tags = request.args.getlist("tags")
    bands = [
        band.to_dict()
        for band in Band.query.filter_by(genre_id=genre_id, theme=theme)
        .filter(Band.tags.any(Tag.name.in_(tags)))
        .all()
    ]

    return jsonify(bands=bands)
