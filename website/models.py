# -- From the website directory import the db variable and get the UserMixin module from the flask-login extension --
from . import db
from flask_login import UserMixin

# -- Define a User model with fields for id, email, password, and username --
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))