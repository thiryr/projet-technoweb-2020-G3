"""class for static methods around the Recipe table"""


from datetime import date
from typing import List

from app import db
from app.models.recipe import Recipe
from app.models.recipe_elements.ingredient import Ingredient
from app.models.recipe_elements.step import Step
from app.models.recipe_elements.utensil import Utensil

from app.repositories.tags import name_to_tag, add_tag
from app.repositories.taglinks import add_taglink

#from app.repositories.recipe_elements.ingredients import get_ingredients_of
#from app.repositories.recipe_elements.utensils import get_utensils_of
#from app.repositories.recipe_elements.steps import get_steps_of



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
        tag = name_to_tag(tag_text)
        #add it if it doesn't exist
        if tag is None:
            tag = add_tag(tag_text)
        new_link = add_taglink(tag.id, recipe.id)
        db.session.add(new_link)
        db.session.commit()

def remove_recipe(recipeid: int) -> None:
    """removes a recipe and all associated links
    Args:
        recipeid ([type]): [description]
    """
    """
    ingredients = get_ingredients_of(recipeid)
    utensils = get_steps_of(recipeid)
    steps = get_steps_of(recipeid)

    for ingredient in ingredients:
        db.session.delete(ingredient)
    for step in steps:
        db.session.delete(step)
    for utensil in utensils:
        db.session.delete(utensil)
        """
    #TODO FINISH THIS
    

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


def get_pinned_recipes() -> List[Recipe]:
    """Returns a list of all pinned recipes
    """
    return Recipe.query.filter_by(pinned=True).all()