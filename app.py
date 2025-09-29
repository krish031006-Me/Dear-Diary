""" This is the main file for the web app 
    It contains all the web routes and all the backend logic that will run"""

# Including all the libraries
from flask import Flask, render_template, Session, request, redirect, flash
from CS50 import SQL
from helpers import login_required
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
@app.route("/login", method = ["GET", "POST"])
def login():
    # if method is GET
    if request.method == "GET":
        return render_template("login.html")
    # if method is POST
    else: 
        ...

# This is the register route
@app.route("/register", method = ["GET", "POST"])
def register():
    # if method is GET
    if request.method == "GET":
        return render_template("register.html")
    # if method is POST
    else:
        ...

# This is the trends route to show trends 
@app.route("/trends")
@login_required
def trends():
    # if method is GET
    if request.method == "GET":
        return render_template("trends.html")
    # if method is POST
    else:
        ...

# This is the route to open a writing space
@app.route("/space")
@login_required
def space():
    # if method is GET
    if request.method == "GET":
        return render_template("space.html")
    # if method is POST
    else:
        ...

# This is the route for stats page
@app.route("/stats")
@login_required
def stats():
    # if method is GET
    if request.method == "GET":
        return render_template("stats.html")
    # if method is POST
    else:
        ...

# This is the history route
@app.route("/history")
@login_required
def history():
    # if method is GET
    if request.method == "GET":
        return render_template("history.html")
    # if method is POST
    else:
        ...

# This is the sharing route for the entries if needed
@app.route("/share")
@login_required
def share():
    # if method is GET
    if request.method == "GET":
        return render_template("share.html")
    # if method is POST
    else:
        ...
    
# Calling the app.py
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)