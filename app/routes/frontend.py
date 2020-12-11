"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from app.models.recipe import Recipe
from flask import Blueprint, render_template

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')


@website.route('/')
def index_page():
    """
    Page d'accueil
    """
    recipe = Recipe('Poulet rôti', 4, 2, True, '2020-01-09', 0,
                    'https://assets.afcdn.com/recipe/20200227/108291_w1024h1024c1cx1824cy2736.webp')
    return render_template('pages/recipe.html', theme='dark', user=True, r1=recipe)


@website.route('/light')
def index_page_light():
    recipe = Recipe('Poulet rôti', 4, 2, True, '2020-01-09', 0,
                    'https://assets.afcdn.com/recipe/20200227/108291_w1024h1024c1cx1824cy2736.webp')
    return render_template('pages/recipe.html', theme='light', user=True, r1=recipe)




@website.route('/login')
def login():
    return '<h1>Sign in now !</h1>'

# TODO add routes here with "website" instead of "app"
