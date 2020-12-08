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

    image_url = Column(st.String(512), nullable=True)

    portion_number = Column(st.Integer, nullable=False)
    difficulty = Column(st.Integer, nullable=False)
    is_public = Column(st.Boolean, nullable=False)

    publicated_on = Column(st.Date, nullable=False)

    category_id = Column(st.Integer, ForeignKey('category.id'), nullable=False)

    # Init
    # By default, permissions are that of a regular user
    def __init__(self, name: str, portion_number: int, difficulty: int, is_public: bool, publicated_on: str, category_id: int, image_url=None):
        self.name = name

        self.portion_number = portion_number
        self.difficulty = difficulty
        self.is_public = is_public

        self.publicated_on = parse_date(publicated_on)

        self.image_url = image_url

        self.category_id = category_id


def parse_date(date: str) -> datetime.date:
    """
    parses string to python date format
    """
    return datetime.datetime.strptime(date, "%Y-%d-%m").date()
