"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from werkzeug.utils import secure_filename
from app.forms import RegisterForm, SignInForm, ValidationError, EditProfileForm
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

import app.repositories.users as user_rep
import app.repositories.ratings as rating_rep
import app.repositories.favorites as fav_rep
import app.repositories.recipes as recipe_rep
import app.repositories.recipe_elements.ingredients as ing_rep
import app.repositories.recipe_elements.utensils as uten_rep
import app.repositories.recipe_elements.steps as step_rep
import app.repositories.subscriptions as sub_rep
import app.repositories.usergroups as group_rep
import app.repositories.categories as cat_rep
import app.repositories.taglinks as taglink_rep

import app.models.subscription as sub_model
import app.models.user as user_model
import app.models.recipe as recipe_model
import app.models.rating as rating_model
import app.models.category as cat_model
import app.models.usergroup as usergroup_model

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')

# ROUTES #

# Home
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/')
def home_page():
    return render_template('pages/index.html', page='home', theme=get_theme(current_user), user=get_user_infos(current_user))

# Log In
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home_page'))

    form = SignInForm()
    if form.validate_on_submit():
        if user_rep.find_user_by_username(form.username.data) is not None:
            user = user_rep.find_user_by_username(form.username.data)
        elif user_rep.find_user_by_mail(form.username.data) is not None:
            user = user_rep.find_user_by_mail(form.username.data)
        else:
            user = None

        if user is None or not user.check_password(form.password.data):
            form.password.errors.append(
                'Identifiant ou mot de passe invalide.')
            return redirect(url_for('frontend.login'))

        if not group_rep.find_group_by_id(user.user_group).can_login:
            form.password.errors.append(
                "Vous n'avez pas le droit de vous connectez.")
            return redirect(url_for('frontend.login'))

        login_user(user)

        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('frontend.home_page')

        return redirect(next_page)

    return render_template('pages/formpage.html', theme=get_theme(current_user), user=False, form=form)

# Log out
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('frontend.home_page'))

# Register
# A MODIFIER


@website.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.home_page'))

    form = RegisterForm()
    if form.validate_on_submit():
        print("OK")
        try:
            new_user = user_rep.add_user(username=form.username.data, password=form.password.data,
                                         mail=form.email.data, birthdate=form.birthday.data, first_name=form.first_name.data, last_name=form.last_name.data)
            return redirect(url_for('frontend.login'))
        except ValidationError as e:
            form.username.errors.append(e)

    return render_template('pages/formpage.html', theme=get_theme(current_user), user=False, form=form)

# Recipe
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/recipe/<int:id>')
def recipe_page(id):
    return render_template('pages/recipe.html', theme=get_theme(current_user), user=get_user_infos(current_user), recipe=get_recipe_infos(current_user, id))

# Recipes
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/my-recipes')
@login_required
def my_recipes_page():
    return render_template('pages/my-recipes.html', page='my-recipes', title="Mes recettes", theme=get_theme(current_user), user=get_user_infos(current_user))

# Edit recipe
# A MODIFIER


@website.route('/edit-recipe', methods=['GET', 'POST'])
@login_required
def edit_recipe_page():
    return render_template('pages/edit-recipe.html', theme=get_theme(current_user), user=get_user_infos(current_user))

# Profile
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile_page(id):
    return render_template('pages/profile.html', theme=get_theme(current_user), user=get_user_infos(current_user), viewed_user=get_viewed_user_infos(current_user, id))


@website.route('/profile', methods=['GET'])
@login_required
def own_profile_page():
    return render_template('pages/profile.html', theme=get_theme(current_user), user=get_user_infos(current_user), viewed_user=get_viewed_user_infos(current_user, current_user.id))


# Edit profile
# OK POUR MOI, MODIFIER SI BESOIN
@website.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_page():
    form = EditProfileForm()

    if form.validate_on_submit():
        try:
            user_rep.edit_profile(
                form.username.data,
                form.password.data,
                form.email.data,
                form.first_name.data,
                form.last_name.data, 
                form.birthday.data,
                form.picture.data,
                current_user.id
            )

            return redirect('profile/%d' % current_user.id)
        except ValueError as e:
            if 'pseudo' in str(e):
                form.username.errors.append(e)
            elif 'email' in str(e):
                form.email.errors.append(e)

    else:
        # Fill form with existing data
        form.username.data = current_user.username
        form.email.data = current_user.mail
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.birthday.data = current_user.birthdate
        form.picture.data = current_user.avatar_url


    return render_template('pages/formpage.html', theme=get_theme(current_user), user=get_user_infos(current_user), form=form)

# Users
# MODIFIER SI BESOIN


@website.route('/users')
@login_required
def users_page():
    if group_rep.find_group_by_id(current_user.user_group).is_admin:
        return render_template('pages/users.html', theme=get_theme(current_user), page='users', user=get_user_infos(current_user), users=get_all_users_infos(), groups=get_all_group_infos())
    return redirect(url_for('frontend.home_page'))

# Subscriptions
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/subscriptions')
@login_required
def subscriptions_page():
    return render_template('pages/sorted.html', page='subscriptions', title='Abonnements', theme=get_theme(current_user), user=get_user_infos(current_user))

# Favorites
# OK POUR MOI, MODIFIER SI BESOIN


@website.route('/favorites')
@login_required
def favorites_page():
    return render_template('pages/sorted.html', page='favorites', title='Recettes favorites', theme=get_theme(current_user), user=get_user_infos(current_user))

# Search
# A MODIFIER


@website.route('/search')
def search_page():
    return render_template('pages/sorted.html', page='search', title='Résultat de la recherche', theme=get_theme(current_user), user=get_user_infos(current_user))

# 404 error
# OK POUR MOI, MODIFIER SI BESOIN


@website.route("/<path:invalid_path>")
def error_page(*args, **kwargs):
    # TODO get color theme and user
    return render_template('pages/404.html', theme=get_theme(current_user), user=get_user_infos(current_user)), 404

# FUNCTIONS #


def get_theme(user):
    # function which returns the current user's theme ; Returns dark theme by default if no user is logged in

    if user.is_authenticated:
        if user.dark_mode:
            return 'dark'
        else:
            return 'light'
    return 'dark'


def get_user_infos(user):
    # function which returns a dictionary containing the current user's basic infos, or False if the user is not authenticated

    if user.is_authenticated:
        dict = {}

        dict['user_id'] = user.id

        # Check if user is chef
        if group_rep.find_group_by_id(user.user_group).name == 'chef':
            dict['is_chef'] = True
        else:
            dict['is_chef'] = False

        # Check if user is admin
        dict['is_admin'] = group_rep.find_group_by_id(user.user_group).is_admin

        # Check avatar url
        dict['avatar_url'] = user.avatar_url

        return dict

    return False


def get_all_group_infos():
    # function which returns a list of dictionaries containing all group infos

    group_list = []
    usergroups = usergroup_model.UserGroup.query.all()

    for group in usergroups:
        group_dict = {}

        group_dict['name'] = group.name
        group_dict['value'] = group.id

        group_list.append(group_dict)

    return group_list


def get_all_users_infos():
    # function which returns a list of dictionaries containing all user infos

    dict_list = []

    users = user_model.User.query.all()

    for u in users:
        user_dict = {}

        # username
        user_dict['pseudo'] = u.username

        # ranking
        user_dict['ranking'] = user_rep.get_average_user_rating_for(u.id)

        # full name
        user_dict['name'] = display_name('', u.first_name, u.last_name)

        # avatar url
        user_dict['avatar_url'] = u.avatar_url

        # usergroup
        user_dict['usergroup'] = group_rep.find_group_by_id(u.user_group).name

        # profile url
        user_dict['profile_url'] = '/profile/%d' % u.id

        dict_list.append(user_dict)

    return dict_list


def get_viewed_user_infos(user, id):
    # function which returns a dictionary containing the viewed user's profile infos
    viewed_user = user_rep.find_user_by_id(id)
    dict = {}

    # username
    dict['pseudo'] = viewed_user.username

    # ranking
    # A VERIFIER
    dict['ranking'] = user_rep.get_average_user_rating_for(viewed_user.id)

    # full name
    dict['name'] = display_name('', viewed_user.first_name, viewed_user.last_name)

    # avatar url
    dict['avatar_url'] = viewed_user.avatar_url

    # birthdate
    if viewed_user.birthdate is None:
        bd = ''
    else:
        bd = str(viewed_user.birthdate)
    dict['birthday'] = viewed_user.birthdate

    # is chef
    if group_rep.find_group_by_id(viewed_user.user_group).name == 'chef':
        dict['is_chef'] = True
    else:
        dict['is_chef'] = False

    # is admin
    dict['is_admin'] = group_rep.find_group_by_id(
        viewed_user.user_group).is_admin

    # nb subscribers
    dict['nb_subscribers'] = sub_rep.get_subscriptions_to(viewed_user.id)

    # current user is subscribed
    if current_user.is_anonymous:
        dict['current_user_is_subscribed'] = False
    else:
        if sub_rep.get_specific_subscription(user.id, viewed_user.id) is None:
            dict['current_user_is_subscribed'] = False
        else:
            dict['current_user_is_subscribed'] = True

    # recipes
    dict['recipes'] = []
    viewed_recipes = recipe_rep.get_recipe_from_user(viewed_user.id)
    for r in viewed_recipes:
        current_recipe = {}
        current_recipe['name'] = r.name
        current_recipe['average_rating'] = r.average_score
        current_recipe['picture'] = r.image_url
        current_recipe['url'] = '/recipe/%s' % r.id
        current_recipe['nb_favorites'] = r.follow_number

        favorited = False
        if not current_user.is_anonymous:
            favorited = fav_rep.user_has_favorite(user.id, r.id)

        current_recipe['current_user_favorited'] = favorited

        dict['recipes'].append(current_recipe)

    return dict


def get_recipe_infos(user, id):
    # function which returns a dictionary containing the viewed recipe's infos

    recipe = recipe_rep.get_recipe_from_id(id)

    author = user_rep.find_user_by_id(recipe.author)

    dict = {}

    # title
    dict['title'] = recipe.name

    # author name
    dict['author_name'] = display_name(
        author.username, author.first_name, author.last_name)
    # author url
    dict['author_url'] = '/profile/%d' % author.id

    # is chef
    if group_rep.find_group_by_id(author.user_group).name == 'chef':
        dict['author_is_chef'] = True
    else:
        dict['author_is_chef'] = False

    # average rating
    dict['average_rating'] = recipe.average_score

    # fav count
    dict['fav_count'] = recipe.follow_number

    # difficulty
    dict['difficulty'] = recipe.difficulty

    # target people -> C'EST BIEN PORTION NUMBER ?
    dict['target_people'] = recipe.portion_number

    # is public
    dict['is_public'] = recipe.is_public

    # is pinned
    dict['is_pinned'] = recipe.pinned

    # category -> ID OU NOM DE LA CATEGORIE ?
    dict['category'] = recipe.category_id

    # tags
    dict['tags'] = taglink_rep.get_recipe_tags(recipe.id)

    # user is author
    if user == author:
        dict['current_user_is_author'] = True
    else:
        dict['current_user_is_author'] = False

    # user has favorite
    favorited = False
    if not current_user.is_anonymous:
        favorited = fav_rep.user_has_favorite(user.id, recipe.id)

    dict['current_user_favorited'] = favorited

    # ingredients
    dict['ingredients'] = ing_rep.get_ingredients_as_string_of(recipe.id)

    # utensils
    dict['ustensiles'] = uten_rep.get_utensils_as_string_of(recipe.id)

    # picture
    dict['picture'] = recipe.image_url

    # steps
    dict['steps'] = step_rep.get_steps_as_string_of(recipe.id)

    # rated by user
    has_rating = False
    if not current_user.is_anonymous:
        has_rating = rating_rep.user_has_rating(user.id, recipe.id)
    dict['already_rated_by_current_user'] = has_rating

    # comments
    dict['comments'] = []
    comments = rating_rep.get_ratings_to(recipe.id)
    for c in comments:
        comment_author = user_rep.find_user_by_id(c.user_id)

        current_comment = {}
        current_comment['user_id'] = c.user_id
        current_comment['comment_id'] = c.id
        current_comment['avatar_url'] = comment_author.avatar_url
        current_comment['username'] = display_name(
            comment_author.username, comment_author.first_name, comment_author.last_name)
        current_comment['rating'] = c.value
        current_comment['message'] = c.comment

        dict['comments'].append(current_comment)

    return dict


def display_name(pseudo, first_name, last_name):

    if not first_name and not last_name:
        return pseudo.strip(' ')
    else:
        # Filter out none values
        first_name = first_name if first_name != None else ''
        last_name = last_name if last_name != None else ''

        return " ".join((first_name, last_name)).strip(' ')
