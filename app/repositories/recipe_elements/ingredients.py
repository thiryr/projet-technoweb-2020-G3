"""class for static methods around the Ingredient table"""

import app.repositories.recipes as recipe_rep
from app import db

from app.models.recipe_elements.ingredient import Ingredient

from typing import List


def get_ingredients_as_string_of(recipeid: int) -> List[str]:
    """
    Returns a list of all the ingredients as strings, if they exist

    Raises:
    can pass ValueError from get_ingredients_of if invalid recipeid
    """
    return list(map(lambda ingObject: ingObject.text, get_ingredients_of(recipeid)))

def get_ingredients_of(recipeid: int) -> List[Ingredient]:
    if recipe_rep.get_recipe_from_id(recipeid) is None:
        raise ValueError(f"Tried to get the ingredients of non-existant recipe {recipeid}")
    return Ingredient.query.filter_by(recipe_id=recipeid).all()