"""
This file contains the definition of the "api" blueprint containing
all the routes related to the api (CRUD operations on the database).
"""

from flask import Blueprint, redirect, request
from flask_login.utils import login_required, login_user, logout_user


from app.repositories.users import UserRepository
from app.repositories.subscriptions import SubscriptionRepository

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def ping():
    return 'OK'


# Login
@api.route('/login', methods=['POST'])
def login():
    user = UserRepository.find_user_by_username('admin')
    password = 'admin'

    if user == None:
        return 'No such user', 400

    if not user.check_password(password):
        return 'Password did not match', 400

    login_user(user)
    return redirect('/')


@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()


# example for extracting data from the url path
@api.route('/new/<int:name>')
@login_required
def create(name: int):
    return f'Created nb {name} !'


# User-related operations

@api.route('/user/create', methods=['POST'])
def create_user():
    UserRepository.add_user("Bob", "123", "bob@bob.com")
    return redirect("/")


@api.route('/user/update_role', methods=['POST'])
def update_user_group():
    # if not current_user.is_admin:
    #    return 'You do not have the necessary permissions'

    UserRepository.find_user_by_username("Bob").set_user_group("admin")

    # send to previous page if possible, index otherwise
    if request.referrer:
        return redirect(request.referrer)
    return redirect("/")


# Subscription-related operations

@api.route('/subscription/create', methods=['POST'])
def create_subscription():
    try:
        SubscriptionRepository.add_subscription(1, 2)
    except ValueError:
        return 'Invalid user ids', 400
    except Exception as e:
        return 'Could not commit changes', 500

    # send to previous page if possible, index otherwise
    if request.referrer:
        return redirect(request.referrer)
    return redirect("/")

# TODO add routes here with "api" instead of "app"
