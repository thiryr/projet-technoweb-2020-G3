"""class for static methods around the Rating table"""

import app.repositories.recipes as recipe_rep
import app.repositories.users as user_rep
import app.repositories.usergroups as usergroup_rep
from app import db

import app.models.rating as rating_model

from typing import List


MIN_SCORE = 0
MAX_SCORE = 5


    
def get_ratings_from(userid: int) -> List[rating_model.Rating]:
    """
    Returns all favorites from a user, or None
    """
    user = user_rep.find_user_by_id(userid)
    if user is None:
        raise ValueError("User does not exist")
    if usergroup_rep.find_group_by_id(user.user_group) != usergroup_rep.find_group_by_name('chef'):
        raise ValueError("User is not a chef")
    return rating_model.Rating.query.filter_by(user_id=userid).all()

def get_average_rating_for(recipeid: int) -> int:
    """Gives the average of all ratings for a recipe
    Args:
        recipeid (int): a valid recipe id
    Returns:
        int: the average of ratings or 0 if no rating OR invalid recipeid
    """
    #get ratings or no rating if invalid id
    try:
        ratings = get_ratings_to(recipeid)
    except ValueError:
        ratings = []
    #compute average
    rating_sum = 0
    rating_count = 0
    for rating in ratings:
        rating_sum+=rating.value
        rating_count+=1
    if rating_count!=0:
        average_rating = int(round(rating_sum/rating_count))
    else:
        average_rating = 0
    return average_rating

def get_ratings_to(recipeid: int) -> List[rating_model.Rating]:
    """
    Returns a list of ratings to that recipe id, or None
    """
    return rating_model.Rating.query.filter_by(recipe_id=recipeid).all()

def get_ratings_number_to(recipeid: int) -> int:
    """Gives the number of ratings for a given recipe

    Args:
        recipeid (int): a valid recipe id

    Returns:
        int: the number of ratings
    """
    return rating_model.Rating.query.filter_by(recipe_id=recipeid).count()

def get_specific_rating(userid: int, recipeid:int) -> rating_model.Rating:
    """
    Returns the specified rating instance, or None
    """
    return rating_model.Rating.query.filter_by(user_id=userid, recipe_id=recipeid).first()

def add_rating(userid: int, recipeid:int, score:int, comment: str) -> rating_model.Rating:
    """
    Adds a rating to the table, provided it is valid
    if one of the targets doesn't exist
    Arguments: valid userid and recipeid, a score from 0 to 5, a comment as a string
    Returns: the created rating
    """
    #no double rating
    if get_specific_rating(userid,recipeid) is not None:
        raise ValueError(f"Rating from user {userid} to recipe {recipeid} already exists")
    #score domain
    if score<MIN_SCORE or score>MAX_SCORE:
        raise ValueError(f"Score should be in integer range [0,5], was {score}")
    user = user_rep.find_user_by_id(userid)
    recipe = recipe_rep.get_recipe_from_id(recipeid)
    #check that they exist
    if user is None:
        raise ValueError(f"User did not exist, ID: {userid}")
    if recipe is None:
        raise ValueError(f"Recipe did not exist, ID: {recipeid}")
    new_rating = rating_model.Rating(user_id=userid, recipe_id=recipeid, value=score, comment=comment)
    db.session.add(new_rating)
    db.session.commit()
    #update the average_score of the recipe
    recipe.average_score = get_average_rating_for(recipe.id)
    db.session.commit()
    return new_rating

def remove_rating(rating_id: int) -> None:
    """Removes a subscription with some id from the database
    """
    rating = rating_model.Rating.query.get(rating_id)
    if rating is None:
        print("WARNING: Tried to remove a non-existant favorite")
        return
    db.session.delete(rating)
    db.session.commit()

def update_rating_score(rating_id: int, new_score: int) -> None:
    """Removes a subscription with some id from the database
    """
    if new_score<MIN_SCORE or new_score>MAX_SCORE:
        raise ValueError(f"Score should be in integer range [0,5], was {new_score}")
    rating = rating_model.Rating.query.get(rating_id)
    if rating is None:
        print("WARNING: Tried to remove a non-existant favorite")
        return
    rating_model.Rating.value = new_score
    db.session.commit()

def update_rating_comment(rating_id: int, new_comment: str) -> None:
    """Removes a subscription with some id from the database
    """
    rating = rating_model.Rating.query.get(rating_id)
    if rating is None:
        print("WARNING: Tried to remove a non-existant favorite")
        return
    rating_model.Rating.comment = new_comment
    db.session.commit()

def user_has_rating(user_id: int, recipe_id:int) -> bool:
    """Tells whether or not a user already has a rating
    Args:
        user_id (int): a valid user id
        recipe_id (int): a valid recipe id
    Returns:
        bool: True if rating exists
    """
    if get_specific_rating(user_id, recipe_id) is None:
        return False
    return True