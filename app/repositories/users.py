"""This file defines several functions to handle a group of Users"""

from app import db, login_manager

from app.models.user import User


    
def add_user(username: str, password: str, mail: str, usergroup='regular', avatar_url = "https://i.stack.imgur.com/l60Hf.png")->User:
    if find_user_by_username(username) is not None:
        raise ValueError('A user already uses that username')
    if find_user_by_mail(mail) is not None:
        raise ValueError('A user already uses that mail address')
    # Create a new user
    new_user = User(username, password, mail, usergroup, avatar_url)
    # Add it to the database
    db.session.add(new_user)
    db.session.commit()
    return User

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

def set_user_darkmode(userid:int, darkmode=True) -> None:
    """sets the specified user's visual mode

    Args:
        userid (int): a valid user id
        darkmode (bool, optional): True to set theme to dark. Defaults to True.
    """

    user = find_user_by_id(userid)

    #absolutely non-critical, just issue a warning and keep going
    if user is None:
        print("WARNING: User did not exist")
        return
    
    user.dark_mode = darkmode
    
    db.session.commit()