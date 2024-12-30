# -- Initialize the imports --
from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user

# -- Define the views blueprint --
views = Blueprint("views", __name__)

# -- Define the home route --
@views.route("/", methods = ["GET", "POST"])
# -- Login is required to access home --
@login_required
# -- Define the home method --
def home():
        # -- Render the home template to the user --
        return render_template("home.html")