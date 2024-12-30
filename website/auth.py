# -- Initialize the imports --
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# -- Define the "auth" blueprint --
auth = Blueprint("auth", __name__)

# -- Define the login route --
@auth.route("/login/", methods = ["GET", "POST"])
# -- Define the login method --
def login():
    # -- If user is already logged in, redirect to the home page --
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    # -- Otherwise check if the http request method is POST and get the credentials from the forms --
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        rememberMeBool = request.form.get("rememberme")
        
        # -- Define the user variable to check if the email is in the database --
        user = User.query.filter_by(email = email).first()
        
        # -- If the user exists --
        if user:
            # -- Check if the password matches with the hashed password stored in the database --
            if check_password_hash(user.password, password):
                # -- If it does process the login and redirect the user to the home page --
                flash("Logged in successfully", category = "success")
                login_user(user, remember = True if rememberMeBool is True else False)
                return redirect(url_for("views.home"))
            else:
                # -- Send the message "Incorrect Password" and refresh the page --
                flash("Incorrect password", category = "error")
        else:
            # -- If the user doesn't exist send the message "Email is not in the database" --
            flash("Email is not in the database", category = "error")
    
    # -- Give the user the login page content --    
    return render_template('login.html')

# -- Define the logout route --
@auth.route("/logout/")
# -- Being logged in will be required to log out (common sense) --
@login_required
# -- Define the logout method --
def logout():
    # -- Log out the user and redirect them to the login page to log back in --
    logout_user()
    return render_template("login.html")

# -- Define the sign-up route --
@auth.route("/sign-up/", methods = ["GET", "POST"])

# -- Define the sign-up method --
def sign_up():
    # -- Check if the user is already authenticated, if they are redirect them to the home page --
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    # -- Check if the http request method is POST
    if request.method == "POST":
        # -- Then get the email, password, and confirm password aswell as the rememberMeBool values --
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        rememberMeBool = request.form.get('rememberMe')
        
        # -- Check if the email already exists in the database, if it does, send an error message and refresh the page --
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already in use", category = "error")
        # -- Check if the email is less than four characters long, then send an error message and refresh the page --    
        elif len(email) < 4:
            flash("Email must greater than 4 characters.", category = "error")
        
        # -- Check if the password is less that eight characters long, then send an error message and refresh the page --
        elif len(password1) < 7:
            flash("Password must be greater or equal to 8 characters", category = "error")
        
        # -- Check if the two passwords entered don't match, then send an error message and refresh the page --
        elif password1 != password2:
            flash("Your passwords don't match", category = "error")
        
        # -- If all the checks pass, then create a new user and add them to the database, login them in and redirect them to the home page --
        else:
            # -- Generate a secure password hash using the scrypt method and store the user in the database --
            new_user = User(email = email, password = generate_password_hash(password1, method = "scrypt", salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            # -- Login the user according to the remember me boolean and flash a confirmation message, redirect them to the home page
            if rememberMeBool is True:
                # -- Login the user --
                login_user(user = new_user, remember = True)
                # -- Flash the message --
                flash("Account created!", category = "success")
                # -- Redirect them to the home page --
                return redirect("views.home")
            else:
                # -- Login the user --
                login_user(user = new_user, remember = False)
                # -- Flash the message --
                flash("Account created!", category = "success")
                # -- Redirect them to the home page --
                return redirect("views.home")

    # -- Render the home page to the user --
    return render_template('signup.html')