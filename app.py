""" This is the main file for the web app 
    It contains all the web routes and all the backend logic that will run"""

# Including all the libraries
from flask import Flask, render_template, session, request, redirect, flash, jsonify, url_for
from cs50 import SQL
from flask_session import Session
from helpers import login_required, hashing
from werkzeug.security import check_password_hash
import re
from reflection import control, analyze
import json

# Initialising the Flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.debug = True

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
@app.route("/", methods = ["POST", "GET"])
def dashboard():
    # if the method is get
    if request.method == "GET": 
        # checking if user is logged in or not
        user_id = session.get("user_id") # checking without error

        # For representing stats-
        num = db.execute("SELECT COUNT(*) AS num FROM users WHERE status = 'done'")
        count = num[0]["num"]
        num_entry = db.execute("SELECT COUNT(*) AS num_entry FROM analysis")
        entries = num_entry[0]["num_entry"]

        if not user_id:
            return render_template("dashboard.html", demo=True, users = count, entries = entries)

        # checking if there are enough entries done by the user
        count = db.execute("SELECT COUNT(*) AS count FROM analysis WHERE user_id = ?", (user_id),)
        count = count[0]["count"]
        
        # conditions for count
        if count <= 3:
            return render_template("dashboard.html", demo = True, users = count, entries = entries) # running the demo graphs
        
        # The final return statement
        return render_template("dashboard.html", users = count, entries = entries) # calling the actual graphs
        
    # if it's post
    else:
        return render_template("dashboard.html", users = count, entries = entries)

# This is the login route for the project
@app.route("/login", methods = ["GET", "POST"])
def login():
    # if method is GET
    if request.method == "GET":
        return render_template("login.html")
    # if method is POST
    else: 
        # getting all the values submitted by the user
        email, password = request.form.get("email").lower().strip(), request.form.get("password").strip()
        # Checking for the fields to be filled
        if not any([email, password]):
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
        if not (check_password_hash(hashed, password)):
            flash("Entered password is incorrect.")
            return redirect("/login")
        
        # get the user_id for session
        user_id = user[0]["user_id"]
        session["user_id"] = user_id

        # exiting from the login route
        flash("Logged In successfully.")
        return redirect("/")
        
# This is the register route
@app.route("/register", methods = ["GET", "POST"])
def register():
    # if method is GET
    if request.method == "GET":
        return render_template("register.html")
    # if method is POST
    else:
        # getting all the values submitted by the user
        email, username, password = request.form.get("email").lower().strip(), request.form.get("username").lower().strip(), request.form.get("password").strip()
        # Checking for the fields to be filled
        if not any([email, username, password]):
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
                print("inside")
                flash("Email already in use")
                return redirect("/register")

            # fetching the id for the user
            user_id = db.execute("SELECT user_id FROM users WHERE email = ?", (email),);
            print(user_id)
            session["user_id"] = user_id[0]["user_id"] # setting it up for sessions
            flash("Registered successfully")
            # returning to the dashboard
            return redirect("/")
            
# The logout route
@app.route("/logout")
def logout():
    # This clear the user_id
    session.clear()
    # call the login route
    return redirect("/login")

# This is the route to open a writing space
@app.route("/space", methods = ["POST", "GET"])
@login_required
def space():
    # if method is GET
    if request.method == "GET":
        return render_template("space.html")
    # if method is POST
    else:
        # checking if this is the first entry
        num = db.execute("SELECT COUNT(*) AS num FROM users WHERE user_id = ?", (session["user_id"]),)
        count = num[0]["num"]
        if count == 0:
            db.execute("UPDATE users SET status = 'done' WHERE user_id = ?", (session["user_id"]),)
        # adding the entry to the database storing it
        user_entry = request.form.get("diary_entry")
        db.execute("INSERT INTO entries (user_id, entry) VALUES (?, ?)", session["user_id"], user_entry)
        # calling the analysis function
        whole_entry = db.execute("SELECT * FROM entries WHERE user_id = ? AND` entry = ?", session["user_id"], user_entry)
        try:
            print("outside")
            json = analyze(whole_entry, db)
        except Exception as e:
            print(f"Error running analysis: {e}")
        
        # returning
        flash("Entry saved!")
        return redirect("/")

# This is the history route
@app.route("/history", methods = ["GET", "POST"])
@login_required
def history():
    # getting all the entries done by the user
    entries = db.execute("SELECT * FROM entries WHERE user_id = ? ORDER BY written_date DESC", (session["user_id"]),)
    if entries == []:
        return render_template("history.html")
    # if method is GET
    if request.method == "GET":
        # getting the demo lines  
        few_lines = [] # an empty list for adding few demo lines
        for entry in entries:
            text = entry["entry"]
            few_lines.append(text[:50])

        return render_template("history.html", entries = entries, lines = few_lines)
    # if method is POST
    else:
        # get the entry_id and the user_id hidden in the space.html
        user_id = request.form.get("user_id")
        entry_id = request.form.get("entry_id")
        # returning the template
        return redirect(url_for("open_entry", entry_id=entry_id, user_id = user_id))

# This is the route to open the entry in space.html
@app.route("/open", methods = ["GET", "POST"])
@login_required
def open_entry():
    # fetching the details
    entry_id = request.args.get("entry_id")
    user_id = request.args.get("user_id")

    # fetching the entry
    entry = db.execute("SELECT entry FROM entries WHERE entry_id = ? AND user_id = ?", entry_id, user_id)
    # returning to the template
    entry = entry[0]["entry"]
    return render_template("space.html", entry = entry)

# This is the sharing route for the entries if needed
@app.route("/share", methods = ["GET"])
@login_required
def share():
    # if method is GET
    if request.method == "GET":
        return render_template("share.html")
    # if method is POST
    else:
        ...

# This is the function to call the control fucntion from reflection.py
@app.route("/API", methods = ["POST"])
def call_control():
    # Running if method is post
    if request.method == "POST":
        # Calling control() with error checking
        try:
            # Getting the body of the JSOn object that was sended 
            body = request.get_json()
            # fetching entry text from body
            entry = body.get("entry_text")
            count = body.get("times")
            previous = body.get("reflect_text")
            AI_reflect = control(entry, previous, "llama-3.3-70b", count, db, session["user_id"])
        except Exception as e:
            # returning as a json object
            return jsonify({
                "reflection":f"Error running control: {e}"
            }), 500

        # modifying the return AI refelction before returning    
        AI_reflect = AI_reflect.replace("/", "")
        AI_reflect = AI_reflect.replace("\\", "")
        if '[' in AI_reflect:
            reflect = (AI_reflect.split('['))[0]
        else:
            reflect = (AI_reflect.split('<'))[0]

    
        # returning the reflection from Cerebras call 
        return jsonify({
            "reflection": reflect
        }), 200

# this is the route for sending data to JS when called
@app.route('/analysis', methods = ["GET", "POST"])
def analysis():
    # getting the count of the entries
    count = db.execute("SELECT COUNT(*) AS count FROM analysis WHERE user_id = ? AND date_created >= date('now', 'weekday 0', '-6 days') ORDER BY date_created ASC", (session["user_id"]),)
    count = count[0]["count"]

    # fetching entries based on the count
    if count >= 3:
        entries = db.execute("SELECT * FROM analysis WHERE user_id = ? AND date_created >= date('now', 'weekday 0', '-6 days') ORDER BY date_created ASC", session["user_id"])
    else:
        entries = db.execute("SELECT * FROM analysis WHERE user_id = ? ORDER BY date_created DESC LIMIT 7", (session["user_id"]),)

    # now we turn this list into a json
    json_dict = {f"entry{i+1}": value for i, value in enumerate(entries)}

    json_string = json.dumps(json_dict, indent=2)
    # returning the json_string
    return json_string

# Calling the app.py
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)