"""
This file contains the definition of the "api" blueprint containing
all the routes related to the api (CRUD operations on the database).
"""

from flask import Blueprint
from flask_login.utils import login_required

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def ping():
    return 'OK'


@api.route('/new/<int:name>')
@login_required
def create(name: int):
    return f'Created nb {name} !'

# TODO add routes here with "api" instead of "app"
