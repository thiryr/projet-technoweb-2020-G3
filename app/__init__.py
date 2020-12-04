"""
Configuration file of the Flask Application.

Author: Martin Danhier
"""

from locale import LC_TIME, setlocale

from flask import Flask
from flask_fontawesome import FontAwesome
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Config app
app = Flask(__name__)
app.config.from_object(Config)

# Configure FontAwesome (for icons)
fa = FontAwesome(app)

# Set the locale for date formatting
setlocale(LC_TIME, 'fr_BE')

# Configure login manager
login_manager = LoginManager(app)
login_manager.login_view = "frontend.login"
login_manager.login_message_category = "info"
login_manager.login_message = "You cannot access this page. Please log in to access this page."
login_manager.session_protection = "strong"

# Configure database
db = SQLAlchemy(app)

# We need to import the models, repositories and blueprints here because they import
# "app", "db" and "login_manager" from this file
# pylint: disable=wrong-import-position
from app.models.user import User

# Repositories (classes containing helper functions for a specific table, for example to manage a group of users)

# Blueprints (routers)
from app.routes.api import api
from app.routes.frontend import website

# Create tables from models
db.create_all()

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(website, url_prefix='/')

# Init database if it is empty
# TODO add more init here
# - add a condition (with "and") to check if the default objects exist or not
# - add the init instructions in the body of the if
if User.query.filter_by(username='admin').count() == 0: 
    # Create admin user
    admin_user = User(
        username='admin',
        password='admin'
    )
    # Commit changes
    db.session.add(admin_user)
    db.session.commit()
