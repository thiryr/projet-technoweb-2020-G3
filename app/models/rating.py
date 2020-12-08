"""Model for the rating table, handling the chef rating feature"""

# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

from app import db



class Rating(db.Model): #type: ignore
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)

    value = Column(st.Integer, nullable=False)
    comment = Column(st.Text, nullable=False)

    user_id = Column(st.Integer, ForeignKey('user.id'), nullable=False)
    recipe_id =  Column(st.Integer, ForeignKey('recipe.id'), nullable=False)




    # Init
    def __init__(self, user_id:int, recipe_id:int, value:int, comment:str):
        
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.value = value
        self.comment = comment