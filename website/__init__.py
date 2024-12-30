# -- Initialize the imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# -- Create the database credentials --
db = SQLAlchemy()
DB_NAME = "database.db"

# -- Define the create app funcion --
def create_app():
    # -- Web app and database configuration --
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shuiaggta7w3t26r4'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    # -- Initialize the function imports --
    from .views import views
    from .auth import auth
    
    # -- Register the blueprints --
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    
    # -- Database models imports --
    from .models import User 
    
    # -- Initialize the create database function --
    create_database(app)
    
    # -- Setup the login manager --
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    # -- Initialize the login manager --
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    # -- Return the configured web app --
    return app

# -- Define the create database function --
def create_database(app):
    # -- Check if the database exists --
    if not path.exists('website/' + DB_NAME):
        # -- If not, create the database and tables --
        with app.app_context():
            db.create_all()
            # -- Notify that the process is done --
            print("Created database!")