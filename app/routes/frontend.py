"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from flask import Blueprint, render_template_string
from flask.templating import render_template
from app.repositories.users import UserRepository

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')


@website.route('/')
def index_page():
    """
    Page d'accueil
    """
    return render_template('pages/index.html', theme='dark')


@website.route('/light')
def index_page_light():
    return render_template('pages/index.html', theme='light')


@website.route('/login')
def login():
    return '<h1>Sign in now !</h1>'

# TODO add routes here with "website" instead of "app"
