# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column
import sqlalchemy.sql.sqltypes as st

from app import db



class UserGroup(db.Model):
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    name = Column(st.String(50), unique=True, nullable=False)
    
    can_access_user_page = Column(st.Boolean, nullable=False)
    can_login = Column(st.Boolean, nullable=False)
    is_admin = Column(st.Boolean, nullable=False)
    can_have_public_recipes = Column(st.Boolean, nullable=False)
    can_access_social_features = Column(st.Boolean, nullable=False)
    can_rate= Column(st.Boolean, nullable=False)






    # Init
    # By default, permissions are that of a regular user
    def __init__(self, name: str):
        self.name = name
        self.can_access_user_page = True
        self.can_login = True
        self.is_admin = False
        self.can_have_public_recipes = True
        self.can_access_social_features = True
        self.can_rate = False

    def set_is_admin(self, new_value: bool):
        self.is_admin = new_value
    
    def set_can_login(self, new_value: bool):
        self.can_login = new_value
    
    def set_can_access_user_page(self, new_value: bool):
        self.can_access_social_features = new_value
    
    def set_can_have_public_recipes(self, new_value: bool):
        self.can_have_public_recipes = new_value
    
    def set_can_access_social_features(self, new_value: bool):
        self.can_access_social_features = new_value
    
    def set_can_rate(self, new_value: bool):
        self.can_rate = new_value