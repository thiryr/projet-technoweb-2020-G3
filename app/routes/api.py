"""
This file contains the definition of the "api" blueprint containing
all the routes related to the api (CRUD operations on the database).
"""

from flask import Blueprint
from flask_login.utils import login_required


from app.repositories.users import UserRepository

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def ping():
    return 'OK'


@api.route('/new/<int:name>')
@login_required
def create(name: int):
    return f'Created nb {name} !'






#User-related operations

@api.route('/user/create', methods=['POST'])
def create_user():
    UserRepository.add_user("Bob", "123", "bob@bob.com")
    return redirect("/")

@api.route('/user/update_role', methods=['POST'])
def update_user_rule():
    UserRepository.find_user_by_name("Bob").set_user_group("admin")
    return redirect("/")

# TODO add routes here with "api" instead of "app"
