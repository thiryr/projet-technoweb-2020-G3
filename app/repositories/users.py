"""This file defines several functions to handle a group of Users"""

from datetime import datetime
from app import db, login_manager

import app.models.user as user_model

import app.models.rating as rating_model
import app.models.recipe as recipe_model

import app.repositories.ratings as rating_rep


def add_user(username: str, password: str, mail: str, usergroup: str = 'regular', avatar_url = "https://i.stack.imgur.com/l60Hf.png", birthdate: str = None, first_name = None, last_name = None):
    if find_user_by_username(username) is not None:
        raise ValueError('A user already uses that username')
    if find_user_by_mail(mail) is not None:
        raise ValueError('A user already uses that mail address')
    # Create a new user
    new_user = user_model.User(username, password, mail, usergroup, avatar_url)
    
    if birthdate:
        new_user.birthdate = datetime.strptime(birthdate, '%d/%m/%Y')

    new_user.first_name = first_name
    new_user.last_name = last_name

    # Add it to the database
    db.session.add(new_user)
    db.session.commit()
    return user_model.User

# Tell login_manager that it can use this function as loader


@login_manager.user_loader
def find_user_by_str_id(id: str) -> user_model.User:
    """Finds a user in the list by a str id. (used by login_manager)"""
    return find_user_by_id(int(id))


def find_user_by_id(id: int) -> user_model.User:
    """Finds a user in the list by id
    Args:
        id (str): Id of the user (string repr of an int)
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find the id user in the database, else return None
    return user_model.User.query.get(id)


def find_user_by_username(username: str) -> user_model.User:
    """Finds a user in the list by username
    Args:
        username (str): The name of the user
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find user with this username, or None if there isn't any
    return user_model.User.query.filter_by(username=username).first()


def find_user_by_mail(mail: str) -> user_model.User:
    """Finds a user in the list by username
    Args:
        mail (str): The mail address of the user
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find user with this username, or None if there isn't any
    return user_model.User.query.filter_by(mail=mail).first()


def set_user_darkmode(userid: int, darkmode=True) -> None:
    """sets the specified user's visual mode

    Args:
        userid (int): a valid user id
        darkmode (bool, optional): True to set theme to dark. Defaults to True.
    """

    user = find_user_by_id(userid)

    # absolutely non-critical, just issue a warning and keep going
    if user is None:
        print("WARNING: User did not exist")
        return

    user.dark_mode = darkmode

    db.session.commit()


def edit_profile(username, password, email, first_name, last_name, birthday, picture, user_id):

    user = find_user_by_id(user_id)

    # username check
    if find_user_by_username(username) != None and user.username != username:
        raise ValueError('Ce pseudo est déjà utilisé.')
    else:
        user.username = username

    # password check
    if password != '':
        user.set_password(password)

    # email
    if find_user_by_mail(email) != None and user.mail != email:
        raise ValueError('Cette adresse email est déjà utilisée.')
    else:
        user.mail = email

    # first name
    user.first_name = first_name

    # last name
    user.last_name = last_name

    # birthday
    user.birthdate = birthday

    # picture
    user.avatar_url = picture

    db.session.commit()


def get_average_user_rating_for(userid: int) -> int:
    """Gives the average of all ratings for a user, 0 if none
    Args:
        userid (int): a valid user id
    Returns:
        int: the average of ratings or 0 if no rating OR invalid recipeid
    """
    # get ratings or no rating if invalid id
    try:
        user = find_user_by_id(userid)
    except ValueError:
        return 0

    user_ratings = rating_model.Rating.query.join(
        recipe_model.Recipe, rating_model.Rating.recipe_id == recipe_model.Recipe.id).join(
        user_model.User, user_model.User.id == recipe_model.Recipe.author).distinct().all()

    ratings = map(lambda rate: rate.value, user_ratings)
    # compute average
    rating_sum = 0
    rating_count = 0
    for rating in ratings:
        rating_sum += rating
        rating_count += 1
    if rating_count != 0:
        average_rating = int(round(rating_sum/rating_count))
    else:
        average_rating = 0
    return average_rating
