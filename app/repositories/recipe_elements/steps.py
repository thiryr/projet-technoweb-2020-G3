"""class for static methods around the Step table"""

from app.repositories.recipes import get_recipe_from_id
from app import db

from app.models.recipe_elements.step import Step

from typing import List



def get_ingredients_as_string_of(recipeid: int) -> List[str]:
    """
    Returns a list of all the ingredients as strings, if they exist

    Raises:
    can pass ValueError from get_ingredients_of if invalid recipeid
    """
    return list(map(lambda ingObject: ingObject.text, get_steps_of(recipeid)))

def get_steps_of(recipeid: int) -> List[Step]:
    if get_recipe_from_id(recipeid) is None:
        raise ValueError(f"Tried to get the steps of non-existant recipe {recipeid}")
    return Step.query.filter_by(recipe_id=recipeid).all()

