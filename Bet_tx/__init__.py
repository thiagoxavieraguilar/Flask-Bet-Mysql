
from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the LoginManager instance
login_manager = LoginManager()


# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Name for the database file
DB_NAME = "bet_flask"

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # Set the secret key for the application
    app.config['SECRET_KEY'] = "bet_tx"
    
    # Set the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:root@localhost/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)

    # Import the views module
    from .views import views
    from .auth import auth

    # Register the views blueprint with the application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import the User and Post model
    from .models import User, Bet

    

    # Initialize the LoginManager instance
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the configured Flask application instance
    return app

def create_database(app):
    """Create the database if it does not exist."""
    if not path.exists("bet_tx/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")