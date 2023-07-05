import os
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, url_for, session, g, flash
from models import connect_to_db, User, Band, Album, Song, Like, Genre
from forms import LoginForm, UserForm, GenerateBandForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "tempkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///album_generator"
)
toolbar = DebugToolbarExtension(app)


connect_to_db(app)

#########################################################################################
# Login/Logout/Signup Routes


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

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


def make_name_dict(name):
    """Takes a name and returns a dictionary with first and last name and formats capitalization"""

    name_dict = {}
    name_list = name.split()
    name_dict["first_name"] = name_list[0].capitalize()
    name_dict["last_name"] = name_list[1].capitalize()
    return name_dict


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    if g.user:
        return redirect(url_for("show_homepage"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            return redirect(url_for("show_homepage"))

        flash("Invalid credentials.")
        return redirect(url_for("login"))

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
        return redirect(url_for("show_homepage"))

    form = UserForm()

    if form.validate_on_submit():
        name = make_name_dict(form.name.data)
        user = User.register_user(
            username=form.username.data,
            first_name=name["first_name"],
            last_name=name["last_name"],
            email=form.email.data,
            password=form.password.data,
        )

        do_login(user)
        return redirect(url_for("show_homepage"))

    return render_template("signup.html", form=form)


#########################################################################################


@app.route("/")
def show_homepage():
    return render_template("home.html")
