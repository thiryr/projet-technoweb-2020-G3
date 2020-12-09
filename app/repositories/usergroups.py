"""This file defines several functions to handle the table of UserGroup"""

from app import db
from app.models.usergroup import UserGroup

class UserGroupRepository:
    """This class contains several helper static functions to handle
    actions on the UserGroup table as a whole.

    This repository provides all CRUD operations."""

    @staticmethod
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

    @staticmethod
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
    

    @staticmethod
    def add_usergroup(group_name:str, can_access_user_page=True, can_login = True, is_admin = False, can_have_public_recipes = True, can_access_social_features = True, can_rate = False):
        """
        adds a usergroup
        @arguments mandatory unique name and permissions, permissions are that of a regular user by default
        @raises ValueError if it already exists
        """
        if UserGroupRepository.find_group_by_name(group_name) is not None:
            raise ValueError("A group with this name already exists")
        
        usergroup = UserGroup(group_name, can_access_user_page, can_login, is_admin, can_have_public_recipes, can_access_social_features, can_rate)
        
        db.session.add(usergroup)
        db.session.commit()