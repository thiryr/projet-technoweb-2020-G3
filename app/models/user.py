# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column
import sqlalchemy.sql.sqltypes as st
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    username = Column(st.String(80), unique=True, nullable=False)
    password_hash = Column(st.String(128), nullable=False)

    # Init
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = generate_password_hash(password)

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
