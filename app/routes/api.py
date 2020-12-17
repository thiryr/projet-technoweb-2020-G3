"""
This file contains the definition of the "api" blueprint containing
all the routes related to the api (CRUD operations on the database).
"""

import app.repositories.ratings as rating_rep
import app.repositories.favorites as fav_rep
import app.repositories.recipes as recipe_rep
import app.repositories.recipe_elements.ingredients as ing_rep
import app.repositories.recipe_elements.utensils as uten_rep
import app.repositories.recipe_elements.steps as step_rep
import app.repositories.users as user_rep
import app.repositories.subscriptions as sub_rep
import app.repositories.usergroups as group_rep
import app.repositories.categories as cat_rep

import app.models.subscription as sub_model
import app.models.favorite as fav_model
import app.models.user as user_model
import app.models.recipe as recipe_model
import app.models.rating as rating_model
import app.models.category as cat_model

from app import db



from flask import Blueprint, redirect, request
from flask.wrappers import Response
from flask_login.utils import login_required, login_user, logout_user
from flask_login import current_user

import json

import datetime



# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def ping():
    return 'OK'


# Login
@api.route('/login', methods=['POST','GET'])
def login():
    user = user_rep.find_user_by_username('admin')
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


    user_rep.add_user("Bob", "123", "bob@bob.com")
    return redirect("/")


@api.route('/user/update_role', methods=['POST'])
@login_required
def update_user_group():
    if not current_user.is_admin:
        return 'You do not have the necessary permissions'

    user_rep.find_user_by_username("Bob").set_user_group("admin")

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
    subscribed_user = user_rep.find_user_by_username(subscribed_name)

    #make sure user was found
    if subscribed_user is None:
        return 'Could not resolve username to existing user', 400

    subscribed_id = subscribed_user.id

    try:
        sub_rep.add_subscription(subscriber_id=current_id, subscribed_id=subscribed_id)
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
    subscribed_user = user_rep.find_user_by_username(subscribed_name)

    #make sure user was found
    if subscribed_user is None:
        return 'User does not exist', 400
    
    subscribed_id = subscribed_user.id

    sub = sub_rep.get_specific_subscription(current_id,subscribed_id)
    if sub is None:
        return 'No such subscription existed', 199

    sub_rep.remove_subscription(sub.id)

    return 'Ok', 200



#Recipe-related routes

@api.route('/recipe/new', methods=['POST'])
@login_required
def new_recipe():
    """Adds a recipe

    Arguments:
    expects {'title':str, 'people':int, 'difficulty':int, 'public':bool, 'category':str,
    'ingredients':[str], 'utensils':[str], 'steps':[str], 'tags':[str] }
    """
    current_id = current_user.id
    req_content = request.json

    try:
        title = str(req_content.get('title'))
        people = int(req_content.get('people'))
        difficulty = int(req_content.get('difficulty'))
        public = bool(req_content.get('public'))
        category = str(req_content.get('category'))

        print(req_content.get('ingredients'))
        
        ingredients = [str(i) for i in req_content.get('ingredients')]
        utensils = [str(i) for i in req_content.get('utensils')]
        steps = [str(i) for i in req_content.get('steps')]
        tags = [str(i) for i in req_content.get('tags')]
    except Exception:
        return "could not type-cast some of the values",410
    category = cat_rep.name_to_category(category)
    if category is None:
        return 'Category does not exist',411
    
    category = category.id
    
    try:
        recipe = recipe_rep.add_recipe(title,current_id,people,difficulty,public,category)
    except ValueError:
        return 'One of the main inputs was invalid in some way other than type',413
    except Exception:
        return 'Could not add the recipe',510
    try:
        recipe_rep.compile_recipe(recipe, ingredients, utensils, steps, tags)
    except ValueError:
        return 'One of the elements of the recipe or its tags were invalid',414
    except Exception:
        #remove pre-compile recipe from db
        recipe_rep.remove_recipe(recipe.id)
        return 'Could not compile the recipe',511
    
    return 'ok',200
    
@api.route('/recipe/update_visibility', methods=['POST'])
@login_required
def update_recipe_visibility():
    """Switches visibility between public and private

    Arguments:
        Expects fields 'recipe_id':int and 'public':bool

    Returns:
        json {'public':bool}, http 200
    """
    current_id = current_user.id


    req_content = request.form
    

    #recipe_id field
    recipe_id_field = req_content.get('recipe_id')
    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400
    
    #check recipe validity and user permissions
    recipe = recipe_rep.get_recipe_from_id(recipe_id)
    if recipe is None:
        return 'No such recipe',400
    
    if recipe.author != current_id and not group_rep.find_group_by_id(current_user.user_group).is_admin:
        return 'Insufficient permissions',400


    #visibility field
    public_field = req_content.get('public')
    if public_field is None:
        return 'Missing "public" field',400
    
    try:
        set_public = bool(recipe_id_field)
    except Exception:
        return '"public" should be a boolean',400
    
    try:
        status = recipe_rep.switch_recipe_visibility(recipe_id, set_public)
    except ValueError:
        return 'Invalid input of some sort',400
    except Exception:
        return 'Could not satisfy request',400
    
    return json.dumps({'public':status}),200



@api.route('/recipe/user_recipes', methods=['GET'])
@login_required
def retrieve_user_recipes():
    """Returns all the information necessary to display the user's recipes

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """

    current_id = current_user.id

    recipes = recipe_rep.get_recipe_from_user(current_id)

    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = user_rep.find_user_by_id(recipe.author)
        ratings_average = rating_rep.get_average_rating_for(recipe.id)
        favorite_number = fav_rep.get_favorites_number_to(recipe.id)
        current_favorite = fav_rep.user_has_favorite(current_id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'average_rating': ratings_average, 
        'favorites': favorite_number, 'is_favorite': current_favorite, 'img_url': recipe.image_url})

    return json.dumps({'recipes_info':recipe_jsons})



@api.route('/recipe/get_popular', methods=['GET'])
@login_required
def retrieve_sorted_subs():
    """Returns all the information necessary to display the user's subscription recipes

    Argument: 
        Expects sorting mode '

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """
    current_id = current_user.id

    request_content = request.args

    sorting_mode = request_content.get('sorting_mode')

    recipes_query = recipe_model.Recipe.query.join(sub_model.Subscription, sub_model.Subscription.subscriber_id == current_id 
    and sub_model.Subscription.subscribed_id==recipe_model.Recipe.author
    and (recipe_model.Recipe.is_public or recipe_model.Recipe.author == current_id))

    if sorting_mode is not None and sorting_mode == 'trending':
        recipes = recipes_query.filter(recipe_model.Recipe.publicated_on <= datetime.date.today().replace(day=1)).order_by(recipe_model.Recipe.average_score.desc()).all()
    else:
        recipes = recipes_query.order_by(recipe_model.Recipe.publicated_on.desc()).all()
        
    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = user_rep.find_user_by_id(recipe.author)
        ratings_average = rating_rep.get_average_rating_for(recipe.id)
        favorite_number = fav_rep.get_favorites_number_to(recipe.id)
        current_favorite = fav_rep.user_has_favorite(current_id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'author_id': int(author.id), 'author_chef': True,
         'average_rating': ratings_average, 'favorites': favorite_number, 'is_favorite': current_favorite, 
         'img_url': recipe.image_url})



    return json.dumps({'recipes_info':recipe_jsons})

@api.route('/recipe/subscription_sorted', methods=['GET'])
@login_required
def retrieve_sorted_subs():
    """Returns all the information necessary to display the user's subscription recipes

    Argument: 
        Expects sorting mode 'trending'/'recent', assumes current_user

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """
    current_id = current_user.id

    request_content = request.args

    sorting_mode = request_content.get('sorting_mode')

    recipes_query = recipe_model.Recipe.query.join(sub_model.Subscription, sub_model.Subscription.subscriber_id == current_id 
    and sub_model.Subscription.subscribed_id==recipe_model.Recipe.author
    and (recipe_model.Recipe.is_public or recipe_model.Recipe.author == current_id))

    if sorting_mode is not None and sorting_mode == 'trending':
        recipes = recipes_query.filter(recipe_model.Recipe.publicated_on <= datetime.date.today().replace(day=1)).order_by(recipe_model.Recipe.average_score.desc()).all()
    else:
        recipes = recipes_query.order_by(recipe_model.Recipe.publicated_on.desc()).all()
        
    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = user_rep.find_user_by_id(recipe.author)
        ratings_average = rating_rep.get_average_rating_for(recipe.id)
        favorite_number = fav_rep.get_favorites_number_to(recipe.id)
        current_favorite = fav_rep.user_has_favorite(current_id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'author_id': int(author.id), 'author_chef': True,
         'average_rating': ratings_average, 'favorites': favorite_number, 'is_favorite': current_favorite, 
         'img_url': recipe.image_url})



    return json.dumps({'recipes_info':recipe_jsons})

@api.route('/recipe/search_sorted', methods=['GET'])
def retrieve_sorted_search():
    """Returns all the information necessary to display the recipes in some order

    Argument: 
        Expects sorting mode 'trending'/'recent', assumes current_user

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """
    search_term = request.args.get('search_term')
    if search_term is None:
        search_term = ""

    recipes_query = recipe_rep.search(search_term)

    sorting_mode = request.args.get('sorting_mode')

    if sorting_mode is not None and sorting_mode == 'trending':
        recipes = recipes_query.filter(recipe_model.Recipe.publicated_on <= datetime.date.today().replace(day=1)).order_by(recipe_model.Recipe.average_score.desc()).all()
    else:
        recipes = recipes_query.order_by(recipe_model.Recipe.publicated_on.desc()).all()
        
    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = user_rep.find_user_by_id(recipe.author)
        ratings_average = rating_rep.get_average_rating_for(recipe.id)
        favorite_number = fav_rep.get_favorites_number_to(recipe.id)
        if current_user.is_anonymous:
            current_favorite = False
        
        else:
            current_favorite = fav_rep.user_has_favorite(current_user.id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'author_id': int(author.id), 'author_chef': True,
         'average_rating': ratings_average, 'favorites': favorite_number, 'is_favorite': current_favorite, 
         'img_url': recipe.image_url})


    return json.dumps({'recipes_info':recipe_jsons})



@api.route('/recipe/favorites_sorted', methods=['GET'])
@login_required
def retrieve_sorted_favs():
    """Returns all the information necessary to display the user's favorite recipes

    Argument: 
        Expects sorting mode 'trending'/'recent', assumes current_user

    Returns: json {'recipes_info':
    [{'recipe_id': int, 'recipe_name': str, 'author_nick': str, 'author_first': str, 'author_last': str, 
    'average_rating': int, 'favorites': int, 'is_favorite': bool, 'img_url':str},..]}
    """
    current_id = current_user.id

    request_content = request.args

    sorting_mode = request_content.get('sorting_mode')

    recipes_query = recipe_model.Recipe.query.join(fav_model.Favorite, fav_model.Favorite.user_id == current_id and recipe_model.Recipe.id==fav_model.Favorite.recipe_id and recipe_model.Recipe.is_public)

    if sorting_mode is not None and sorting_mode == 'trending':
        recipes = recipes_query.filter(recipe_model.Recipe.publicated_on <= datetime.date.today().replace(day=1)).order_by(recipe_model.Recipe.average_score.desc()).all()
    else:
        recipes = recipes_query.order_by(recipe_model.Recipe.publicated_on.desc()).all()
        
    recipe_jsons = []

    for recipe in recipes:
        #get key elements
        author = user_rep.find_user_by_id(recipe.author)
        ratings_average = rating_rep.get_average_rating_for(recipe.id)
        favorite_number = fav_rep.get_favorites_number_to(recipe.id)
        current_favorite = fav_rep.user_has_favorite(current_id, recipe.id)


        recipe_jsons.append({'recipe_id': recipe.id, 'recipe_name': recipe.name, 'author_nick': author.username, 
        'author_first': author.first_name, 'author_last': author.last_name, 'author_id': int(author.id), 'author_chef': True,
         'average_rating': ratings_average, 'favorites': favorite_number, 'is_favorite': current_favorite, 
         'img_url': recipe.image_url})

    return json.dumps({'recipes_info':recipe_jsons})

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
    fav = fav_rep.get_specific_favorite(current_id, recipe_id)
    #if none, add it
    if fav is None:
        try:
            fav_rep.add_favorite(current_id, recipe_id)
        except Exception:
            return 'Could not add a favorite',500
        is_favorite = True
    else:
        try:
            fav_rep.remove_favorite(fav.id)
        except Exception:
            return 'Could not remove this favorite',500
        is_favorite = False
    
    return json.dumps({'is_favorite':is_favorite}),200


#Review-related (Rating-related) routes

@api.route('/ratings/add', methods=['POST'])
@login_required
def add_review():
    """Adds a rating for a specific recipe from the currently logged-in user
    Arguments:
        Expects a recipe identifier "recipe_id"
        a comment "comment"
        a score "score"
    Returns:
        200 'ok' if alright
    """

    

    #request to dict
    req_content = request.form
    
    #retrieve recipe_id
    recipe_id_field = req_content.get('recipe_id')

    if recipe_id_field is None:
        return 'Missing recipe_id field',400
    
    #convert to int
    try:
        recipe_id = int(recipe_id_field)
    except Exception:
        return 'recipe_id should be integer',400
    

    #retrieve score
    score_field = req_content.get('score')

    if score_field is None:
        return 'Missing score field',400
    
    #convert to int
    try:
        score = int(score_field)
    except Exception:
        return 'score should be integer',400
    
    if score<1 or score>5:
        return 'score should be between 1 and 5',400
    
    #retrieve comment
    comment = req_content.get('comment')

    if comment is None:
        return 'Missing comment field',400

    

    

    recipe = recipe_rep.get_recipe_from_id(recipe_id)

    if recipe is None:
        return 'No such recipe',400

    current_id = current_user.id
    try:
        rating_rep.add_rating(current_id,recipe_id,score=score,comment=comment)
    except ValueError:
        return 'User already has a review for that recipe or information was invalid'
    except Exception:
        return 'Could not add a review',500

    return 'ok',200
    
