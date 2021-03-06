"""class for static methods around the Recipe table"""


from datetime import date
from typing import List

from app import db
from app.models.recipe import Recipe
from app.models.recipe_elements.ingredient import Ingredient
from app.models.recipe_elements.step import Step
from app.models.recipe_elements.utensil import Utensil

import app.repositories.tags as tag_rep
import app.repositories.taglinks as taglink_rep


import app.repositories.favorites as fav_rep
import app.repositories.ratings as rating_rep

import app.repositories.recipe_elements.ingredients as ing_rep
import app.repositories.recipe_elements.utensils as uten_rep
import app.repositories.recipe_elements.steps as step_rep




def search(word: str):
    """
    Should return all recipes matching some search term (look up tags and categories too..)
    """
    #TODO

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
        tag = tag_rep.name_to_tag(tag_text)
        #add it if it doesn't exist
        if tag is None:
            tag = tag_rep.add_tag(tag_text)
        new_link = taglink_rep.add_taglink(tag.id, recipe.id)
        db.session.add(new_link)
        db.session.commit()

def remove_recipe(recipeid: int) -> None:
    """removes a recipe and all associated links
    Args:
        recipeid ([type]): [description]
    """
    
    recipe = get_recipe_from_id(recipeid)
    if recipe is None:
        print('WARNING: Tried to remove a non-existant recipe')
        return
    
    ingredients = ing_rep.get_ingredients_of(recipeid)
    utensils = uten_rep.get_utensils_of(recipeid)
    steps = step_rep.get_steps_of(recipeid)

    for ingredient in ingredients:
        db.session.delete(ingredient)
    for step in steps:
        db.session.delete(step)
    for utensil in utensils:
        db.session.delete(utensil)
    
    favorites = fav_rep.get_favorites_to(recipeid)
    for favorite in favorites:
        fav_rep.remove_favorite(favorite.id)
    
    ratings = rating_rep.get_ratings_to(recipeid)
    for rating in ratings:
        rating_rep.remove_rating(rating.id)
    


    db.session.delete(recipe)
    
    db.session.commit()


def pin_recipe(recipeid: int) -> None:
    """Sets a recipe as pinned to the front page
    Args:
        recipeid (int): valid recipe id
    """
    recipe = get_recipe_from_id(recipeid)
    if recipe.pinned:
        print("WARNING: Tried to pin an already-pinned recipe")
    else:
        recipe.pinned = True
        db.session.commit()

def unpin_recipe(recipeid: int) -> None:
    """Removes pinned state from recipe if it was
    Args:
        recipeid (int): valid recipe id
    """
    recipe = get_recipe_from_id(recipeid)
    if not recipe.pinned:
        print("WARNING: Tried to unpin a recipe that already was not")
    else:
        recipe.pinned = False
        db.session.commit()

def switch_recipe_visibility(recipeid: int, set_public: bool) -> bool:
    """Modifies visibility of the recipe ("private"/"public")

    Args:
        recipeid (int): valid receipe id
        set_public (bool): whether to set public or not
    
    Returns:
        new status
    """

    recipe = get_recipe_from_id(recipeid)
    if recipe is None:
        raise ValueError(f"Tried to switch visibility of non-existant recipe {recipeid}")
    
    recipe.is_public = set_public
    db.session.commit()

    return recipe.is_public

#GET
#recipe

def get_recipe_from_id(recipe_id: int) -> Recipe:
    """Returns the recipe based on the id, or None
    """
    return Recipe.query.get(recipe_id)




def get_recipe_from_user(user_id: int) -> List[Recipe]:
    """Returns all the recipes written by a user, ordered by date
    """
    return Recipe.query.filter_by(author=user_id).order_by(Recipe.publicated_on.desc()).all()



def get_top_recipes(recipe_number = 20, up_to=date.today().replace(day=1)) -> List[Recipe]:
    """Returns a list of the recipes in order of their score
    Args:
        number (int, optional): the number of recipes to fetch. Defaults to 20.
        up_to (date, optional): the maximum date for a recipe. Defaults to the first day of the current month.
    """
    return Recipe.query.filter(Recipe.publicated_on<=up_to).order_by(Recipe.average_score.desc(), Recipe.follow_number.desc()).all()[:recipe_number]

def get_n_recipes(recipe_number = 20, up_to=date(2020,1,1), newest_first=False) -> List[Recipe]:
    """Gives all recipes to to some date (first day of 2020 by default)

    Args:
        recipe_number (int, optional): limit number of recipes in the list. Defaults to 20
        up_to (date, optional): limit date. Defaults to first day of 2020
        newest_first (boolean, optional): True for newest to oldest. Defaults to True

    Returns:
        List[Recipe]: list of recipe in order of date
    """
    default_query = Recipe.query.filter(Recipe.publicated_on<=up_to)
    if newest_first:
        query = default_query.order_by(Recipe.average_score.desc())
    else:
        query = default_query.order_by(Recipe.average_score.asc())
    
    return query.all()[:recipe_number]
    
def get_pinned_recipes() -> List[Recipe]:
    """Returns a list of all pinned recipes
    """
    return Recipe.query.filter_by(pinned=True).all()