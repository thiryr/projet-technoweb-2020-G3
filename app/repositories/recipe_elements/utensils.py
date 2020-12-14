"""class for static methods around the Ingredient table"""

from app.repositories.recipes import get_recipe_from_id
from app import db

from app.models.recipe_elements.utensil import Utensil

from typing import List


def get_utensils_as_string_of(recipeid: int) -> List[str]:
    """
    Returns a list of all the utensils as strings, if they exist
    """
    return list(map(lambda utenObject: utenObject.text, get_utensils_of(recipeid)))

def get_utensils_of(recipeid: int) -> List[Utensil]:
    if get_recipe_from_id(recipeid) is None:
        raise ValueError(f"Tried to get the utensils of non-existant recipe {recipeid}")
    return Utensil.query.filter_by(recipe_id=recipeid).all()
