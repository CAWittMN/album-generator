import os
from flask import Flask, render_template, redirect, url_for, session, g
from models import connect_to_db, User, Band, Album, Song, Like, Genre

app = Flask(__name__)

app.config["SECRET_KEY"] = "TEMP"

CURR_USER_KEY = 'curr_user'


with app.app_context(app):
    connect_to_db(app)

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
        

@app.route("/")
def show_homepage():
    return render_template("home.html")


@app.route('/login')
def login():