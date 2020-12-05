# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column
import sqlalchemy.sql.sqltypes as st

from app import db



class Tag(db.Model):
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    
    name = Column(st.String(20), nullable=False, unique=True)






    # Init
    def __init__(self, name:str):
        self.name = name
        