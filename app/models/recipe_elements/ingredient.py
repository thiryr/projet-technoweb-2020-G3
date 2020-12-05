# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

from app import db



class Ingredient(db.Model):
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    text = Column(st.String(32), nullable=False)

    recipe_id =  Column(st.Integer, ForeignKey('recipe.id'), nullable=False)




    # Init
    def __init__(self, text:str, recipe_id:int):
        
        self.recipe_id = recipe_id
        self.text = text
