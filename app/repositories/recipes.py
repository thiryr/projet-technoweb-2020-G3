from app import db
from app.models.recipe import Recipe
from app.models.recipe_elements.ingredient import Ingredient
from app.models.recipe_elements.step import Step
from app.models.recipe_elements.utensil import Utensil 

class RecipeRepository:

    @staticmethod
    def search(word: str):
        """
        Should return all recipes matching some search term (look up tags and categories too..)
        """
        pass


    @staticmethod
    def add_recipe(name: str, portion_number:int, difficulty:int, is_public:bool, publicated_on:str, category_id:int, image_url=None)->Recipe:
        """
        Adds a recipe to the table
        @Returns the recipe added
        """

        new_recipe = Recipe(name , portion_number, difficulty, is_public, publicated_on, category_id, image_url)
        
        db.session.add(new_recipe)
        
        db.session.commit()
        
        return new_recipe
    
    @staticmethod
    def compile_recipe(recipe: Recipe, ingredients: [str], utensils: [str], steps: [str]):
        """
        Adds components of the recipe in the tables
        """

        #create and add the elements
        for ingredient_text in ingredients:
            additional_ingredient = Ingredient(ingredient_text, recipe.id)
            db.session.add(additional_ingredient)
        
        for utensil_text in utensils:
            additional_utensil = Utensil(utensil_text, recipe.id)
            db.session.add(additional_utensil)
        
        for step_text in ingredients:
            additional_step = Step(step_text, recipe.id)
            db.session.add(additional_ingredient)
        
        
        db.session.commit()
    
