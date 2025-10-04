""" This is the helpers file which will contain all the supporting function for the web app"""

# importing the necessary files
from flask import session, redirect
from functools import wraps
from werkzeug.security import generate_password_hash

# This is the function to check if the user is logged in or not 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Checking if the user_id is not stored in session
        if session.get("user_id") == None:
            return redirect("/login")
        # if the id is stored i.e the user is logged in
        else:
            return f(*args, **kwargs)
    return decorated_function
        
# This is the function for password hashing
def hashing(password):
    # Converting the passoword to a hashed password
    return generate_password_hash(password)