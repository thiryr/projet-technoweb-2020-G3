"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from flask import Blueprint, render_template_string
from app.repositories.users import UserRepository

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')


@website.route('/')
def ping():
    user = UserRepository.find_user_by_id(1)
    return render_template_string('<h1>Hello {{name}}</h1>', name=user.username)


@website.route('/login')
def login():
    return '<h1>Sign in now !</h1>'

# TODO add routes here with "website" instead of "app"
