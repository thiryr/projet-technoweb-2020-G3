"""class for static methods around the Ingredient table"""

from app.repositories.recipes import RecipeRepository
from app import db

from app.models.recipe_elements.utensil import Utensil

from typing import List


class UtensilRepository:

    @staticmethod
    def get_ingredients_of(recipeid: int) -> List[str]:
        """
        Returns a list of all the utensils as strings, if they exist
        """
        if RecipeRepository.get_recipe_from_id(recipeid) is None:
            raise ValueError(f"Tried to get the ingredients of non-existant recipe {recipeid}")

        return list(map(lambda utenObject: utenObject.text, Utensil.query.filter_by(recipe_id=recipeid).all()))

