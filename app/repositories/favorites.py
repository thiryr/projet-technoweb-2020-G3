"""class for static methods around the Favorite table"""

import app.repositories.recipes as recipe_rep
import app.repositories.users as user_rep
from app import db

import app.models.favorite as favorite_model

from typing import List


    
def get_favorites_from(userid: int) -> List[favorite_model.Favorite]:
    """
    Returns all favorites from a user, or None
    """
    return favorite_model.Favorite.query.filter_by(user_id=userid).all()

def get_favorites_to(recipeid: int) -> List[favorite_model.Favorite]:
    """
    Returns a list of favorites to that recipe id, or None
    """
    return favorite_model.Favorite.query.filter_by(recipe_id=recipeid).all()


def get_favorites_number_to(recipeid: int) -> int:
    """
    Returns the number of favorites to that recipe id
    """
    return favorite_model.Favorite.query.filter_by(recipe_id=recipeid).count()


def get_specific_favorite(userid: int, recipeid:int) -> favorite_model.Favorite:
    """
    Return the specified favorite instance, or None
    """
    return favorite_model.Favorite.query.filter_by(user_id=userid, recipe_id=recipeid).first()

def user_has_favorite(userid:int, recipeid:int) -> bool:
    """Returns true if the user has favorited that recipe
    """
    if get_specific_favorite(userid,recipeid) is None:
        return False
    return True

def add_favorite(userid: int, recipeid:int) -> favorite_model.Favorite:
    """
    Adds a favorite to the table, provided it is valid
    if one of the targets doesn't exist
    Returns: the created favorite
    """
    #no double favorite
    if get_specific_favorite(userid,recipeid) is not None:
        raise ValueError(f"Favorite from user {userid} to recipe {recipeid} already exists")
    user = user_rep.find_user_by_id(userid)
    recipe = recipe_rep.get_recipe_from_id(recipeid)
    #check that they exist
    if user is None:
        raise ValueError(f"User did not exist, ID: {userid}")
    if recipe is None:
        raise ValueError(f"Recipe did not exist, ID: {recipeid}")
    new_fav = favorite_model.Favorite(userid, recipeid)
    recipe.follow_number+=1
    db.session.add(new_fav)
    db.session.commit()
    return new_fav

def remove_favorite(fav_id: int) -> None:
    """Removes a subscription with some id from the database
    """
    fav = favorite_model.Favorite.query.get(fav_id)
    if fav is None:
        print("WARNING: Tried to remove a non-existant favorite")
        return
    
    #update follow_number
    recipe = recipe_rep.get_recipe_from_id(fav.recipe_id)
    recipe.follow_number -= 1
    assert recipe.follow_number>=0
    
    db.session.delete(fav)
    db.session.commit()