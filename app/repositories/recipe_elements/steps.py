"""class for static methods around the Step table"""

from app.repositories.recipes import RecipeRepository
from app import db

from app.models.recipe_elements.step import Step

from typing import List


class StepRepository:

    @staticmethod
    def get_ingredients_of(recipeid: int) -> List[str]:
        """
        Returns a list in order of all the steps as strings, if they exist
        """
        if RecipeRepository.get_recipe_from_id(recipeid) is None:
            raise ValueError(f"Tried to get the ingredients of non-existant recipe {recipeid}")

        return list(map(lambda stepObject: stepObject.text, Step.query.filter_by(recipe_id=recipeid).order_by(Step.order_in_recipe).all()))

