""" This is the main file for the web app 
    It contains all the web routes and all the backend logic that will run"""

# Including all the libraries
from flask import Flask, render_template, Session, request, redirect, flash
from CS50 import SQL

# Initialising the Flask app
app = Flask(__name__)
app.debug = True
app.config("TEMPLATES_AUTO_RELOAD")

# Setting up the sessions
app.config["SESSION_PERMANENT"] = False # not storing the session permanently
app.config["SESSION_TYPE"] = "filesystem" # storing sessions inside of filesystem
# Initialising the app for use
Session(app)

# the database of users
db = SQL("sqlite:///users.db")

# This is the route to control responses
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache" # it doesn't allows to store dynamic cache.
    return response

# the main dashboard route
@app.route("/")
def dashboard():
    ...

# This is the login route for the project
@app.route("/login")
def login():
    ...

# This is the register route
@app.route("/register")
def register():
    ...

# This is the trends route to show trends 
@app.route("/trends")
def trends():
    ...

# This is the route to open a writing space
@app.route("/space")
def space():
    ...

# This is the route for stats page
@app.route("/stats")
def stats():
    ...

# This is the history route
@app.route("/history")
def history():
    ...

# This is the sharing route for the entries if needed
@app.route("/share")
def share():
    ...

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)