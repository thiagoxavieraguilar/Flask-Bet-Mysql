from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os 

load_dotenv()
# Create the SQLAlchemy database instance
db = SQLAlchemy()

DB_NAME = os.environ.get('DB_NAME') 

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # Set the secret key for the application
    app.config['SECRET_KEY'] = "bet_tx"

    # Configure the app to connect to MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:root@127.0.0.1/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database instance
    db.init_app(app)

    with app.app_context():
        # Import models here to ensure tables are created when app is run
        from . import models

    # Import the views module
    from .views import views
    from .auth import auth

    # Register the views blueprint with the application
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Initialize the LoginManager instance
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Return the configured Flask application instance
    return app
