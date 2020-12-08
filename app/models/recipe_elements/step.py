"""Model for the step table, containing the steps for a specific recipe"""

# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

from app import db



class Step(db.Model): #type: ignore
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    text = Column(st.Text, nullable=False)

    recipe_id =  Column(st.Integer, ForeignKey('recipe.id'), nullable=False)




    # Init
    def __init__(self, text:str, recipe_id:int):
        
        self.recipe_id = recipe_id
        self.text = text
