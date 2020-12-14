"""
This file contains the definition of the "api" blueprint containing
all the routes related to the api (CRUD operations on the database).
"""

from app.repositories.ratings import *
from app.repositories.favorites import *
from app.repositories.recipes import *
from app.repositories.recipe_elements.ingredients import *
from app.repositories.recipe_elements.utensils import *
from app.repositories.recipe_elements.steps import *




from flask import Blueprint, redirect, request
from flask.wrappers import Response
from flask_login.utils import login_required, login_user, logout_user
from flask_login import current_user

import json


from app.repositories.users import *
from app.repositories.subscriptions import *

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def ping():
    return 'OK'


# Login
@api.route('/login', methods=['POST','GET'])
def login():
    user = find_user_by_username('admin')
    password = 'admin'

    if user == None:
        return 'No such user', 400

    if not user.check_password(password):
        return 'Password did not match', 400

    login_user(user)
    return redirect('/')


@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()


# example for extracting data from the url path
@api.route('/new/<int:name>')
@login_required
def create(name: int):
    return f'Created nb {name} !'


# User-related operations

@api.route('/user/create', methods=['POST'])
def create_user():
    """Creates a user
    """


    add_user("Bob", "123", "bob@bob.com")
    return redirect("/")


@api.route('/user/update_role', methods=['POST'])
@login_required
def update_user_group():
    if not current_user.is_admin:
        return 'You do not have the necessary permissions'

    find_user_by_username("Bob").set_user_group("admin")

    # send to previous page if possible, index otherwise
    if request.referrer:
        return redirect(request.referrer)
    return redirect("/")


# Subscription-related operations

@api.route('/subscription/create', methods=['POST'])
@login_required
def create_subscription():
    """adds a subscription from the current user to a another user
    Arguments:
        Expects a name in post header
    Returns:
        200 response if ok
    """
    #request to dict
    req_content = request.form

    #retrieve name
    subscribed_name = str(req_content.get('username'))

    current_id = current_user.id
    subscribed_user = find_user_by_username(subscribed_name)

    #make sure user was found
    if subscribed_user is None:
        return 'Could not resolve username to existing user', 400

    subscribed_id = subscribed_user.id

    try:
        add_subscription(subscriber_id=current_id, subscribed_id=subscribed_id)
    except ValueError:
        return 'Invalid user ids in the server', 500
    except Exception as e:
        return f'Could not commit changes: {e.args}', 500

    return 'Ok', 200



@api.route('/subscription/remove', methods=['POST'])
@login_required
def remove_subscription():
    """adds a subscription from the current user to a another user
    Arguments:
        Expects a name in post header
    Returns:
        200 response if ok
    """
    #request to dict
    req_content = request.form
    
    #retrieve name
    subscribed_name = str(req_content.get('username'))

    current_id = current_user.id
    subscribed_user = find_user_by_username(subscribed_name)

    #make sure user was found
    if subscribed_user is None:
        return 'User does not exist', 400
    
    subscribed_id = subscribed_user.id

    sub = get_specific_subscription(current_id,subscribed_id)
    if sub is None:
        return 'No such subscription existed', 199

    remove_subscription(sub.id)

    return 'Ok', 200



#Recipe-related routes

@api.route('/recipe/user_recipes', methods=['POST'])
@login_required
def retrieve_user_recipes():
    """Returns all the information necessary to display the user's recipes

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """

    current_id = current_user.id

    recipes = get_recipe_from_user(current_id)

    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = find_user_by_id(recipe.author)
        ratings_average = get_average_rating_for(recipe.id)
        favorite_number = get_favorites_number_to(recipe.id)
        current_favorite = user_has_favorite(current_id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'average_rating': ratings_average, 
        'favorites': favorite_number, 'is_favorite': current_favorite, 'img_url': recipe.image_url})

    return json.dumps({'recipes_info':recipe_jsons})



@api.route('/recipe/get_info', methods=['POST'])
def retrieve_recipe_info():
    """Returns all ingredients for a recipe

    Arguments:
    Expects a specific recipe id as 'recipe_id' field

    Returns: json {'recipe_id': int, 'recipe_name': str, 'img_url': str, 
    'author_nick': str, 'author_first': str, 'author_last': str, 
    'favorites':int, 'rating': int}
    """

    #request to dict
    req_content = request.form
    
    recipe_id_field = req_content.get('recipe_id')
    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400
    
    recipe = get_recipe_from_id(recipe_id)
    if recipe is None:
        return 'recipe_id does not correspond to any recipe',400

    favorite_nb = get_favorites_number_to(recipe_id)
    average_rating = get_average_rating_for(recipe_id)
    
    img_url = recipe.image_url

    author = find_user_by_id(recipe.author)
    author_nick = author.username
    author_first = author.first_name
    author_last = author.last_name

    return json.dumps({'recipe_id':recipe.id, 'recipe_name': recipe.name, 'img_url':img_url,
    'author_nick': author_nick, 'author_first': author_first, 'author_last': author_last, 
    'favorites':favorite_nb, 'rating': average_rating})

@api.route('/recipe/get_ingredients', methods=['POST'])
def retrieve_ingredients():
    """Returns all ingredients for a recipe

    Arguments:
    Expects a specific recipe id as 'recipe_id' field

    Returns: json {ingredients:[str]}
    """

    #request to dict
    req_content = request.form
    
    recipe_id_field = req_content.get('recipe_id')
    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400

    try:
        ingredients = get_ingredients_of(recipe_id)
    except ValueError:
        return 'recipe_id might have been invalid',400
    except Exception:
        return 'Something went wrong',500

    return json.dumps({'ingredients':ingredients})


@api.route('/recipe/get_steps', methods=['POST'])
def retrieve_steps():
    """Returns all steps for a recipe in order

    Arguments:
    Expects a specific recipe id as 'recipe_id' field

    Returns: json {steps:[str]}
    """

    #request to dict
    req_content = request.form
    
    recipe_id_field = req_content.get('recipe_id')
    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400

    try:
        steps = get_steps_of(recipe_id)
    except ValueError:
        return 'recipe_id might have been invalid',400
    except Exception:
        return 'Something went wrong',500

    return json.dumps({'steps':steps})


@api.route('/recipe/get_utensils', methods=['POST'])
def retrieve_utensils():
    """Returns all utensils for a recipe

    Arguments:
    Expects a specific recipe id as 'recipe_id' field

    Returns: json {utensils:[str]}
    """

    #request to dict
    req_content = request.form
    
    recipe_id_field = req_content.get('recipe_id')
    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400

    try:
        utensils = get_utensils_of(recipe_id)
    except ValueError:
        return 'recipe_id might have been invalid',400
    except Exception:
        return 'Something went wrong',500

    return json.dumps({'utensils':utensils})

@api.route('/recipe/get_reviews', methods=['POST'])
def retrieve_reviews():
    """Returns all the reviews

    Arguments:
    Expects a specific recipe id as 'recipe_id' field

    Returns: json {reviews:[{'text':str,'score':int}]}
    """

    #request to dict
    req_content = request.form
    
    recipe_id_field = req_content.get('recipe_id')

    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400

    try:
        ratings = get_ratings_to(recipe_id)
    except ValueError:
        return 'recipe_id might have been invalid',400
    except Exception:
        return 'Something went wrong',500
    

    reviews = []
    for review in ratings:
        review_text = review.comment
        review_score = review.value
        reviews.append({'text':review_text,'score':review_score})


    return json.dumps({'reviews':reviews})




#Favorite-related routes

@api.route('/favorite/switch', methods=['POST'])
@login_required
def switch_favorite():
    """Adds or removes the favorite between the current user and the specified recipe
    Arguments:
        Expects a recipe identifier
    Returns:
        A json of type {'is_favorite':bool} where is_favorite is true if a favorite was added
    """
    #request to dict
    req_content = request.form
    
    #retrieve recipe_id
    recipe_id_str = str(req_content.get('recipe_id'))

    try:
        recipe_id = int(recipe_id_str)
    except Exception:
        return 'recipe_id should be an integer',400

    current_id = current_user.id

    #Try to get the favorite
    fav = get_specific_favorite(current_id, recipe_id)
    #if none, add it
    if fav is None:
        try:
            add_favorite(current_id, recipe_id)
        except Exception:
            return 'Could not add a favorite',500
        is_favorite = True
    else:
        try:
            remove_favorite(fav.id)
        except Exception:
            return 'Could not remove this favorite',500
        is_favorite = False
    
    return json.dumps({'is_favorite':is_favorite}),200
