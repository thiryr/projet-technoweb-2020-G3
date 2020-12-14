"""class for static methods around the Recipe table"""


from datetime import date
from typing import List

from app import db
from app.models.recipe import Recipe
from app.models.category import Category # viens d'etre rajouter
from app.models.tag import Tag # viens d'etre rajouter
from app.models.taglink import TagLink # viens d'etre rajouter
from app.models.recipe_elements.ingredient import Ingredient
from app.models.recipe_elements.step import Step
from app.models.recipe_elements.utensil import Utensil

from app.repositories.tags import TagRepository
from app.repositories.taglinks import TagLinkRepository


class RecipeRepository: #romeo viens d'etre rajouter

    @staticmethod
    def search(word: str):
        """
        Should return all recipes matching some search term (look up tags and categories too..)
        """
        q = db.session.query(
            Recipe,
            Category,
            Ingredient,
            TagLink,
            Tag
        ) \
        .filter(Recipe.category_id == Category.id) \
        .filter(Recipe.id == Ingredient.recipe_id) \
        .filter(Recipe.id == TagLink.recipe_id) \
        .filter(TagLink.Tag_id == Tag.id) \
        .filter(or_(
            word in Recipe.name,
            word in Tag.name,
            word in Ingredient.text,
            word in Category.name)
        ).all()
        
        return q
        """


    @staticmethod
    def add_recipe(name: str, author_id: int, portion_number:int, difficulty:int, 
    is_public:bool, publicated_on:str, category_id:int, image_url=None)->Recipe:
        """
        Adds a recipe to the table
        @Returns the recipe added
        """

        new_recipe = Recipe(name, author_id, portion_number, difficulty, is_public, publicated_on, category_id, image_url)
        
        db.session.add(new_recipe)
        
        db.session.commit()
        
        return new_recipe
    
    @staticmethod
    def compile_recipe(recipe: Recipe, ingredients: List[str], utensils: List[str], steps: List[str], tags: List[str]):
        """Adds components of the recipe in the tables

        Args:
            recipe (Recipe): The recipe to be compiled with
            ingredients (List[str]): a list of the ingredients as strings
            utensils (List[str]): a list of the utensils as strings
            steps (List[str]): a list of the steps in order as they should appear in the recipe as strings
            tags (List[str]): a list of the tags to link to a recipe, as strings
        """

        #create and add the elements
        for ingredient_text in ingredients:
            additional_ingredient = Ingredient(ingredient_text, recipe.id)
            db.session.add(additional_ingredient)

        for utensil_text in utensils:
            additional_utensil = Utensil(utensil_text, recipe.id)
            db.session.add(additional_utensil)

        for step_number, step_text in enumerate(steps):
            additional_step = Step(step_text, step_number, recipe.id)
            db.session.add(additional_step)

        for tag_text in tags:
            #get the tag
            tag = TagRepository.name_to_tag(tag_text)
            #add it if it doesn't exist
            if tag is None:
                tag = TagRepository.add_tag(tag_text)

            new_link = TagLinkRepository.add_taglink(tag.id, recipe.id)
            db.session.add(new_link)
            db.session.commit()
    
    #GET

    #recipe
    @staticmethod
    def get_recipe_from_id(recipe_id: int) -> Recipe:
        """Returns the recipe based on the id, or None
        """
        return Recipe.query.get(recipe_id)

    @staticmethod
    def get_recipe_from_user(user_id: int) -> List[Recipe]:
        """Returns all the recipes written by a user, ordered by date
        """
        return Recipe.query.filter_by(author=user_id).order_by(Recipe.publicated_on).all()
