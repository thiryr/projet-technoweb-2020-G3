"""This file defines several functions to handle a group of Users"""

from app import db, login_manager

from app.models.user import User


    
def add_user(username: str, password: str, mail: str, usergroup='regular'):
    if find_user_by_username(username) != None:
        raise ValueError('A user already uses that username')
    if find_user_by_mail(mail) != None:
        raise ValueError('A user already uses that mail address')
    # Create a new user
    new_user = User(username, password, mail, usergroup)
    # Add it to the database
    db.session.add(new_user)
    db.session.commit()

# Tell login_manager that it can use this function as loader
@login_manager.user_loader
def find_user_by_str_id(id: str) -> User:
    """Finds a user in the list by a str id. (used by login_manager)"""
    return find_user_by_id(int(id))

def find_user_by_id(id: int) -> User:
    """Finds a user in the list by id
    Args:
        id (str): Id of the user (string repr of an int)
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find the id user in the database, else return None
    return User.query.get(id)

def find_user_by_username(username: str) -> User:
    """Finds a user in the list by username
    Args:
        username (str): The name of the user
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find user with this username, or None if there isn't any
    return User.query.filter_by(username=username).first()

def find_user_by_mail(mail: str) -> User:
    """Finds a user in the list by username
    Args:
        mail (str): The mail address of the user
    Returns:
        User: The user if it is found
        None: otherwise
    """
    # Find user with this username, or None if there isn't any
    return User.query.filter_by(mail=mail).first()