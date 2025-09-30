""" This is the main file for the web app 
    It contains all the web routes and all the backend logic that will run"""

# Including all the libraries
from flask import Flask, render_template, Session, request, redirect, flash
from CS50 import SQL
from helpers import login_required, hashing
from werkzeug.security import check_password_hash, generate_password_hash
import re
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
        # getting all the values submitted by the user
        email, username, password = request.get("name").lower().strip(), request.get("email").lower().strip(), request.get("password").lower().strip()
        # Checking for the fields to be filled
        if not any(email, username, password):
            flash("Invalid credentials.")
            return redirect("/register")

        # getting the user
        user = db.execute("SELECT * FROM users WHERE email = ?", (email),)
        # a bit of error checking
        if user == []:
            flash("User doesn't exist please register yourself.")
            return redirect("/register")

        # checking is the user already exists
        if not email == user[0]["email"]:
            flash("The entered email is not registered with us.")
            return redirect("/login")
        
        # checking if the password entered was correct or not
        hashed = user[0]["password"]
        if not (check_password_hash(hashed[0]["password"], password)):
            flash("Entered password is incorrect.")
            return redirect("/login")
        
        # get the user_id for session
        user_id = user[0]["user_id"]
        Session["user_id"] = user_id

        # exiting from the login route
        flash("Logged In successfully.")
        return redirect("/")
        
# This is the register route
@app.route("/register", method = ["GET", "POST"])
def register():
    # if method is GET
    if request.method == "GET":
        return render_template("register.html")
    # if method is POST
    else:
        # getting all the values submitted by the user
        email, username, password = request.get("name").lower().strip(), request.get("email").lower().strip(), request.get("password").lower().strip()
        # Checking for the fields to be filled
        if not any(email, username, password):
            flash("Invalid credentials.")
            return redirect("/register")

        # getting all the users
        users = db.execute("SELECT * FROM users")
        # a bit of error checking 
        if users == []:
            emails = []
        # if the user exists
        else:
            # the email list
            emails = [email for user in users for email in user.get("email", "")]

        # using regular expression to check for valid email pattern
        match = re.match(r"^[\w!#$%&'\*\+-/=\?\^_`{|}~|]+@[A-Za-z0-9-]{1,63}\..+", email, flags=re.IGNORECASE)
        if match == None: # if there is no match
            flash("Entered email is not valid.")
            return redirect("/register")

        # checking if the email is unique
        if email in emails:
            flash("Entered email is already in use. Please Log In")
            return redirect("/register")
        
        # if the email is totally good
        else:
            # Inserting the data as a new user with a bit of error checking
            try:
                db.execute("INSERT INTO users (email, username, password) VALUES(?, ?, ?)", email, username, hashing(password))
            except Exception as e:
                flash("Email already in use")
                return redirect("/register")

            # fetching the id for the user
            user_id = db.execute("SELECT user_id FROM users WHERE email = ? AND password = ?", email, password);
            Session["user_id"] = user_id[0]["user_id"] # setting it up for sessions
            flash("Registered successfully")
            # returning to the dashboard
            return redirect("/")
            
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