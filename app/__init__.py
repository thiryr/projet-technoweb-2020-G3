"""
Configuration file of the Flask Application.

Author: Martin Danhier
"""

from locale import LC_TIME, setlocale

from flask import Flask
from flask.templating import render_template
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
#setlocale(LC_TIME, 'fr_BE')

# Configure login manager
login_manager = LoginManager(app)
login_manager.login_view = "frontend.login" # type: ignore
login_manager.login_message_category = "info"
login_manager.login_message = "You cannot access this page. Please log in to access this page."
login_manager.session_protection = "strong"

# Configure database
db = SQLAlchemy(app)

# We need to import the models, repositories and blueprints here because they import
# "app", "db" and "login_manager" from this file
# pylint: disable=wrong-import-position
from app.models.user import User
from app.models.usergroup import UserGroup
from app.models.recipe import Recipe
from app.models.category import Category

# Repositories (classes containing helper functions for a specific table, for example to manage a group of users)
from app.repositories.users import add_user
from app.repositories.usergroups import add_usergroup
from app.repositories.categories import add_category, name_to_category
from app.repositories.recipes import add_recipe, compile_recipe, search
# Blueprints (routers)
from app.routes.api import api
from app.routes.frontend import website

# Create tables from models
db.create_all()

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(website, url_prefix='/')



#Existence check was moved to repositories
#Exceptions are only ignored here because they're expected to already exist

#groups
try:
    add_usergroup('admin', is_admin=True, can_rate=True, can_access_user_page=True, can_access_social_features=True, can_login=True, can_have_public_recipes=True)
except ValueError:
    pass

try:
    add_usergroup('regular')
except ValueError:
    pass

try:
    add_usergroup('chef')
except ValueError:
    pass


#default user (make sure admin group is added before it)
try:
    add_user(username='admin',password='admin',mail='admin@localhost',usergroup='admin')
except ValueError:
    pass

#categories
try:
    add_category('entree')
except ValueError:
    pass
try:
    add_category('main')
except ValueError:
    pass
try:
    add_category('dessert')
except ValueError:
    pass
try:
    add_category('gouter')
except ValueError:
    pass
try:
    add_category('pastry')
except ValueError:
    pass
try:
    add_category('misc')
except ValueError:
    pass

