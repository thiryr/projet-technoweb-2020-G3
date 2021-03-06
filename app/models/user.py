"""Model for the user table, handling user-specific and login information"""

# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from app.repositories.usergroups import find_group_by_name

from app import db


class User(UserMixin, db.Model): #type: ignore
    # Columns
    #uniques
    id = Column(st.Integer, primary_key=True, autoincrement=True)

    username = Column(st.String(80), unique=True, nullable=False)
    password_hash = Column(st.String(128), nullable=False)
    mail = Column(st.String(255), unique=True, nullable=False)

    avatar_url = Column(st.String(255), nullable=False)

    #foreign key
    user_group = Column(st.Integer, ForeignKey('usergroup.id'), nullable=False)
    
    #nullables
    first_name = Column(st.String(50), nullable=True)
    last_name = Column(st.String(50), nullable=True)
    birthdate = Column(st.Date, nullable=True)


    #display_related
    dark_mode = Column(st.Boolean, nullable=False)




    # Init
    def __init__(self, username: str, password: str, mail: str, usergroup="regular", avatar_url="https://i.stack.imgur.com/l60Hf.png"):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.mail = mail
        self.set_user_group(usergroup)

        self.avatar_url = avatar_url

        #defaults
        self.dark_mode = True

    #password
    def set_password(self, new_password: str):
        self.password_hash = generate_password_hash(new_password)

    def check_password(self, other_password: str):
        """ Checks a given password with the one stored in the user database.

        Parameters
        ---------
        other_password: the password to check (str)

        Returns
        -------
        True if the passwords are the same (bool)
        """
        return check_password_hash(self.password_hash, other_password)

    #usergroup
    def set_user_group(self, group_name: str):
        new_user_group = find_group_by_name(group_name)

        if new_user_group == None:
            raise ValueError(f"Could not set the user's group to {group_name}, the group could not be found")
        else:
            self.user_group = new_user_group.id
    
    #subscriptions

    #recipes