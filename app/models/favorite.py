"""Model for the favorite table, handling the favorite recipes for each user"""

# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

from app import db



class Favorite(db.Model): #type: ignore
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(st.Integer, ForeignKey('user.id'), nullable=False)
    recipe_id =  Column(st.Integer, ForeignKey('recipe.id'), nullable=False)




    # Init
    def __init__(self, user_id:int, recipe_id:int):
        
        self.recipe_id = recipe_id
        self.user_id = user_id
