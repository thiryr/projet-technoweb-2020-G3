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