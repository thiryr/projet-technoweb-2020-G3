"""This file defines several functions to handle the table of UserGroup"""

from app import db
from app.models.usergroup import UserGroup


    
# Tell login_manager that it can use this function as loader
def find_group_by_id(id: int) -> UserGroup:
    """Finds a group from an input id
    Args:
        id (str): Id of the usergroup (string repr of an int)
    Returns:
        UserGroup: The user if it is found
        None: otherwise
    """
    # Find the group in the database, else return None
    return UserGroup.query.get(id)

def find_group_by_name(group_name: str) -> UserGroup:
    """Finds a group from an input name
    Args:
        username (str): The name of the user
    Returns:
        UserGroup: The group if it is found
        None: otherwise
    """
    # Find group with this name, or None if there isn't any
    return UserGroup.query.filter_by(name=group_name).first()


def add_usergroup(group_name:str, can_access_user_page=True, can_login = True, is_admin = False, can_have_public_recipes = True, can_access_social_features = True, can_rate = False):
    """
    adds a usergroup
    @arguments mandatory unique name and permissions, permissions are that of a regular user by default
    @raises ValueError if it already exists
    """
    if find_group_by_name(group_name) is not None:
        raise ValueError("A group with this name already exists")
    usergroup = UserGroup(group_name, can_access_user_page, can_login, is_admin, can_have_public_recipes, can_access_social_features, can_rate)
    db.session.add(usergroup)
    db.session.commit()


def update_name_of_usergroup(group_name:str, group_id: int):
    """
    update the name of one usergroup
    @arguments a unique group_name and a valid group_id
    @raises ValueError if the group doesn't exist or the group_name is taken
    """
    group = find_group_by_id(group_id)
    if group is None:
        raise ValueError(f"Group {group_id} does not exist")
    if find_group_by_name(group_name=group_name) is not None:
        raise ValueError(f"Group name {group_name} is already in use")
    group.name = group_name
    db.session.commit()


def delete_group(group_id:int):
    """
    updat the name of one usergroup
    @arguments mandatory unique name and permissions, permissions are that of a regular user by default
    @raises ValueError if it already exists
    """
    group = find_group_by_id(group_id)
    if group is None:
        print(f"WARNING: tried to delete non-existant group {group_id}")
        return
    db.session.delete(group)
    db.session.commit()