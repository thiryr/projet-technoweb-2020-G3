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
from app.repositories.users import UserRepository
from app.repositories.usergroups import UserGroupRepository
from app.repositories.categories import CategoryRepository
from app.repositories.recipes import RecipeRepository
# Blueprints (routers)
from app.routes.api import api
from app.routes.frontend import website

# Create tables from models
db.create_all()

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(website, url_prefix='/')



# Init database if it is empty
# TODO Remove the start-up clear
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(f'Clearing table {table}')
        session.execute(table.delete())
    session.commit()

clear_data(db.session)


#Existence check was moved to repositories
#Exceptions are only ignored here because they're expected to already exist

#groups
try:
    UserGroupRepository.add_usergroup('admin')
except ValueError:
    pass

try:
    UserGroupRepository.add_usergroup('regular')
except ValueError:
    pass

#default user (make sure admin group is added before it)
try:
    UserRepository.add_user('admin','admin','admin@localhost',usergroup='admin')
except ValueError:
    pass

#categories
try:
    CategoryRepository.add_category('Lunch')
except ValueError:
    pass
try:
    CategoryRepository.add_category('Breakfast')
except ValueError:
    pass
try:
    CategoryRepository.add_category('Dinner')
except ValueError:
    pass




#TESTS
import app.tests.repository_tests.categories_test as cat_test

cat_test.run_all_tests()

#test recipe
cat = CategoryRepository.name_to_category('Lunch').id
reci = RecipeRepository.add_recipe("Steak Frite", author_id=1, portion_number=4, difficulty=1, is_public=True, publicated_on="2020-12-05", category_id=cat)

RecipeRepository.compile_recipe(reci, ingredients=["4 Steaks","1Kg pomme de terres"], 
utensils=["1 grand couteau","une poelle"], steps=["Do the thing"], tags= ["simple","saveur"])
