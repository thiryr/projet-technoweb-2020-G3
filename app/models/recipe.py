"""Model for the recipe table, handling recipe-specific data"""

# Import Column and types directly from sqlalchemy because pylint
# doesn't detect them if we imported them via the "db" object
from sqlalchemy.sql.schema import Column, ForeignKey
import sqlalchemy.sql.sqltypes as st

import datetime

from app import db


class Recipe(db.Model):  # type: ignore
    # Columns
    id = Column(st.Integer, primary_key=True, autoincrement=True)
    name = Column(st.String(50), nullable=False)

    author = Column(st.Integer, ForeignKey('user.id'), nullable=False)

    image_url = Column(st.String(512), nullable=True)

    portion_number = Column(st.Integer, nullable=False)
    difficulty = Column(st.Integer, nullable=False)
    is_public = Column(st.Boolean, nullable=False)

    publicated_on = Column(st.Date, nullable=False)

    category_id = Column(st.Integer, ForeignKey('category.id'), nullable=False)

    pinned = Column(st.Boolean, nullable=False)

    #added for convenience, can be derived
    average_score = Column(st.Integer, nullable=False)
    follow_number = Column(st.Integer, nullable=False)

    # Init
    # By default, permissions are that of a regular user
    def __init__(self, name: str, author_id: int,  portion_number: int, difficulty: int, 
    is_public: bool, category_id: int, image_url=None):
        self.name = name

        self.portion_number = portion_number
        self.difficulty = difficulty
        self.is_public = is_public


        #always created when being created..
        self.publicated_on = datetime.date.today()

        self.image_url = image_url

        self.author = author_id

        self.category_id = category_id


        
        self.pinned = False

        #non-essential (conceptually)
        self.average_score = 0
        self.follow_number = 0
        

        if image_url is None:
            image_url = "https://i2.wp.com/www.foodrepublic.com/wp-content/uploads/2012/05/testkitchen_argentinesteak.jpg?resize=1280%2C%20560&ssl=1"


def parse_date(date: str) -> datetime.date:
    """
    parses string to python date format
    """
    return datetime.datetime.strptime(date, "%Y-%d-%m").date()
