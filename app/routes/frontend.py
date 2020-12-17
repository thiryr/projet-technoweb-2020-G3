"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from app.forms import RegisterForm, SignInForm, ValidationError
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

import app.repositories.users as user_rep

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
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = SignInForm()
    if form.validate_on_submit():
        if user_rep.find_user_by_username(form.username.data) != None:
            user = user_rep.find_user_by_username(form.username.data)
        elif user_rep.find_user_by_mail(form.username.data) != None:
            user = user_rep.find_user_by_mail(form.username.data)
        else:
            user = None

        if user is None or not user.check_password(form.password.data):
            form.password.errors.append('Identifiant ou mot de passe invalide.')
            return redirect(url_for('login'))

        if user.user_group.can_login:
            form.password.errors.append('Impossible de se connecter à votre compte.')
            return redirect(url_for('login'))

        login_user(user)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_page')

        return redirect(next_page)

    return render_template('pages/formpage.html', theme=get_theme(current_user), user=False, form=form)

# Log out
# OK POUR MOI, MODIFIER SI BESOIN
@website.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# Register
# A MODIFIER
@website.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = user_rep.add_user(username=form.username.data, password=form.password.data, 
            mail=form.mail.data, birthdate=form.birthdate.data, first_name=form.first_name.data, last_name=form.last_name.data)
            return redirect(url_for('login'))
        except ValidationError as e:
            form.username.errors.append(e)

    return render_template('pages/formpage.html', theme=get_theme(current_user), user=False, form=form)

# Recipe
# OK POUR MOI, MODIFIER SI BESOIN -> FONCTION get_recipe_infos INCOMPLETE !
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
@website.route('/edit-recipe/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe_page(id):

    return render_template('pages/edit-recipe.html', theme=get_theme(current_user), user=get_user_infos(current_user))

# Profile
# OK POUR MOI, MODIFIER SI BESOIN
@website.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required # LAISSER OU ENLEVER ?
def profile_page(id):
    return render_template('pages/profile.html', theme=get_theme(current_user), user=get_user_infos(current_user), viewed_user=viewed_user_infos(current_user, id))

# Edit profile
# A MODIFIER
@website.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_page():
    form = EditProfileForm()
    return render_template('pages/formpage.html', theme=get_theme(current_user), user=get_user_infos(current_user), form=form)

# Users
# MODIFIER SI BESOIN -> AJOUTER LA FCT get_all_group_infos
@website.route('/users')
@login_required
def users_page():
    return render_template('pages/users.html', theme=get_theme(current_user), page='users', user=get_user_infos(current_user), users=get_all_users_infos(), groups=get_all_group_infos())

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
    return render_template('pages/404.html', theme='dark', user=None), 404

# TODO add routes here with "website" instead of "app"

# TO USE IN ROUTES -> POUR QUE JE SACHE QUOI METTRE #

@website.route('/users', methods=['GET', 'POST'])
def users():
    return render_template('pages/users.html', theme='dark', page='users', user={
        "is_chef": True,
        "is_admin": True,
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, users=[
        {
            "pseudo": "MichelDupont24",
            "ranking": 4,
            "name": "Michel Dupont",
            "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Michel_Cremades.jpg",
            "usergroup": "chef",
            "profile_url": "/profile"
        },
        {
            "pseudo": "Eugène22",
            "ranking": None,
            "name": "Eugène Leblanc",
            "avatar_url": "https://img.gentside.com/article/insolite/salustiano-sanchez-blazquez-est-l-homme-le-plus-vieux-du-monde-a-112-ans_9c4b850336f7a8fcdaa784c4ba49719d77633cde.jpg",
            "usergroup": "chef",
            "profile_url": "/profile"
        },
        {
            "pseudo": "admin",
            "ranking": 5,
            "name": "Le boss",
            "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg",
            "usergroup": "admin",
            "profile_url": "/profile"
        },
        {
            "pseudo": "Mamy",
            "ranking": 3,
            "name": "Mamy Dupont",
            "avatar_url": "https://img.over-blog.com/350x191/4/37/29/52/15---DIVERS/DOSSIER-1/Mamy.jpg",
            "usergroup": "chef",
            "profile_url": "/profile"
        }
    ], groups = [
        {
            "name": "Utilisateur standard",
            "value": "default"
        },
        {
            "name": "Chef cuisinier",
            "value": "chef"
        },
        {
            "name": "Administrateur",
            "value": "admin"
        },
        {
            "name": "Muet",
            "value": "muted"
        },
        {
            "name": "Banni",
            "value": "banned"
        }
    ])

# FUNCTIONS #

# OK POUR MOI, MODIFIER SI BESOIN
def get_theme(user):
    # function which returns the current user's theme ; Returns dark theme by default if no user is logged in
    
    if user.is_authenticated:
        if user.dark_mode:
            return 'dark'
        else:
            return 'light'
    return 'dark'

# OK POUR MOI, MODIFIER SI BESOIN
def get_user_infos(user):
    # function which returns a dictionary containing the current user's basic infos, or False if the user is not authenticated

    if user.is_authenticated:
        dict = {}

        # Check if user is chef
        if user.user_group.name == 'chef':
            dict['is_chef'] = True
        else:
            dict['is_chef'] = False

        # Check if user is admin
        dict['is_admin'] = user.user_group.is_admin

        # Check avatar url
        dict['avatar_url'] = user.avatar_url

        return dict

    return False

# A FAIRE
#def get_all_group_infos():

def get_all_users_infos():
    # function which returns a list of dictionaries containing all user infos

    dict_list = []

    users = User.query.all()

    for u in users:
        user_dict = {}

        # username
        user_dict['pseudo'] = u.username

        # ranking
        user_dict['ranking'] = rep.ratings.get_ratings_from(u.id)

        # full name
        # A VERIFIER SI NOM VIDE EST NONE OU ''
        if u.first_name == None:
            fn = ''
        else:
            fn = u.first_name
        if u.last_name == None:
            ln = ''
        else:
            ln = u.last_name
        user_dict['name'] = '%s %s'%(fn, ln)

        # avatar url
        user_dict['avatar_url'] = u.avatar_url

        # usergroup
        user_dict['usergroup'] = rep.usergroups.find_group_by_id(u.user_group).name

        # profile url
        user_dict['profile_url'] = '/profile/%d'%u.id

        dict_list.append(user_dict)

    return dict_list

# OK POUR MOI, MODIFIER SI BESOIN
def get_viewed_user_infos(user, id):
    # function which returns a dictionary containing the viewed user's profile infos
    viewed_user = rep.users.find_user_by_id(id)
    dict = {}

    # username
    dict['pseudo'] = viewed_user.username

    # ranking
    # A VERIFIER
    dict['ranking'] = rep.ratings.get_ratings_from(viewed_user.id)

    # full name
    # A VERIFIER SI NOM VIDE EST NONE OU ''
    if viewed_user.first_name == None:
        fn = ''
    else:
        fn = viewed_user.first_name
    if viewed_user.last_name == None:
        ln = ''
    else:
        ln = viewed_user.last_name
    dict['name'] = '%s %s'%(fn, ln)

    # avatar url
    dict['avatar_url'] = viewed_user.avatar_url

    # birthdate
    if viewed_user.birthdate == None:
        bd = ''
    else:
        bd = str(viewed_user.birthdate)
    dict['birthday'] = viewed_user.birthdate

    # is chef
    if viewed_user.user_group.name == 'chef':
        dict['is_chef'] = True
    else:
        dict['is_chef'] = False

    # is admin
    dict['is_admin'] = viewed_user.user_group.is_admin

    # nb subscribers
    dict['nb_subscribers'] = rep.subscriptions.get_subscriptions_to(viewed_user.id)

    # current user is subscribed
    if rep.subscriptions.get_specific_subscription(user.id, viewed_user.id) == None:
        dict['current_user_is_subscribed'] = False
    else:
        dict['current_user_is_subscribed'] = True

    # recipes
    dict['recipes'] = []
    viewed_recipes = rep.recipes.get_recipe_from_user(viewed_user.id)
    for r in viewed_recipes:
        current_recipe = {}
        current_recipe['name'] = r.name
        current_recipe['average_rating'] = r.average_score
        current_recipe['picture'] = r.image_url
        current_recipe['url'] = '/recipe/%s'%r.id
        current_recipe['nb_favorites'] = r.follow_number
        current_recipe['current_user_favorited'] = rep.favorites.user_has_favorite(user.id, r.id)

        dict['recipes'].append(current_recipe)

    return dict

# OK POUR MOI, MODIFIER SI BESOIN
def get_recipe_infos(user, id):
    # function which returns a dictionary containing the viewed recipe's infos

    recipe = rep.recipes.get_recipe_from_id(id)
    author = recipe.author
    dict = {}

    # title
    dict['title'] = recipe.name

    # author name
    dict['author_name'] = author.username

    # author url
    dict['author_url'] = '/profile/%d'%author.id

    # is chef
    if author.user_group.name == 'chef':
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
    dict['tags'] = rep.taglink.get_recipe_tags(recipe.id)

    # user is author
    if user == author:
        dict['current_user_is_author'] = True
    else:
        dict['current_user_is_author'] = False

    # user has favorite
    dict['current_user_favorited'] = rep.favorites.user_has_favorite(user.id, recipe.id)

    # ingredients
    dict['ingredients'] = rep.recipe_elements.ingredients.get_ingredients_as_string_of(recipe.id)

    # utensils
    dict['ustensiles'] = rep.recipe_elements.utensils.get_utensils_as_string_of(recipe.id)

    # picture
    dict['picture'] = recipe.image_url

    # steps
    dict['steps'] = rep.recipe_elements.steps.get_steps_as_string_of(recipe.id)

    # rated by user
    dict['already_rated_by_current_user'] = rep.ratings.user_has_rating(user.id, recipe.id)

    # comments
    dict['comments'] = []
    comments = rep.ratings.get_ratings_to(recipe.id)
    for c in comments:
        current_comment = {}
        current_comment['avatar_url'] = rep.users.find_user_by_id(c.user_id).avatar_url
        current_comment['username'] = rep.users.find_user_by_id(c.user_id).username
        current_comment['rating'] = c.value
        current_comment['message'] = c.comment

        dict['comments'].append(current_comment)

    return dict
