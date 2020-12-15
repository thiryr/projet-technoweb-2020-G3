"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from app.forms import EditProfileForm, RegisterForm, SignInForm
from flask import Blueprint, render_template

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')


@website.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('pages/index.html', page='home', theme='dark', user={
        "is_chef": True,
        "is_admin": False,
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    })

@website.route('/recipe')
def recipe_page():
    """
    Page de recettes
    """
    return render_template('pages/recipe.html', theme='dark', user={
        "is_chef": True,
        "is_admin": False,
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, recipe={
        "title": "Steak-frite",
        "author_name": "Mamy Dupont",
        "author_url": "/light",
        "author_is_chef": True,
        "average_rating": 3,
        "fav_count": 45,
        "difficulty": 1,
        "target_people": 4,
        "public": True,
        "category": "Diner",
        "tags": ['Steak', 'Frites', 'Mamy'],
        "current_user_is_author": True,
        "current_user_favorited": True,
        "ingredients": [
            "Steak",
            "250g de frites",
            "1/2 salade",
            "De la béarnaise",
            "2 gros oignons",
            "Sel / Poivre"
        ],
        "ustensiles": [
            "Une poële",
            "Un saladier",
            "Une friteuse",
            "Un plat à frites",
            "Une spatule"
        ],
        "picture": "https://cdn.pratico-pratiques.com/app/uploads/sites/4/2018/08/30183348/steak-frite-sauce-dijonnaise.jpeg",
        "steps": [
            "Préchauffer la friteuse à 170°",
            "Faire fondre du beurre (ou de la margarine) dans la poëlle.",
            "Une fois la graisse chaude, plonger les frites surgelées pour une première cuisson. Après que",
            "minutes, retirer le bac de l'huile.",
            "Prenez le steak et cuisez le dans la poëlle (+/- 1min sur chaque face ? jsp moi faites comme",
            "voulez)",
            "Oubliez pas d'avoir lavé la salade avant de faire tout ça, ensuite mettez de la vinaigraîte e",
            "oignons dedans.",
            "Refaites une cuisson des frites une fois que la température atteint 170° à nouveau.",
            "Faites les étapes que j'ai oublié.",
            "Oui je sais, dans la photo y'a des tomates. Mais bon à mon âge on n'a pas d'appareil photo hein !",
            "Dégustez ! Et alors elle est bonne ou pas la recette de mamy ?"
        ],
        "already_rated_by_current_user": False,
        "comments": [
            {
                "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Michel_Cremades.jpg",
                "username": "Michel Dupont",
                "rating": 4,
                "message": "Coucou mamy, merci pour cette bonne recette. Personnellement, j'ajouterais un peu d'ail sur le steak, mais c'est déjà très bon comme ça."
            },
            {
                "avatar_url": "https://img.gentside.com/article/insolite/salustiano-sanchez-blazquez-est-l-homme-le-plus-vieux-du-monde-a-112-ans_9c4b850336f7a8fcdaa784c4ba49719d77633cde.jpg",
                "username": "Eugène Leblanc",
                "rating": 2,
                "message": "C'est un scandale, de mon temps on cuisinait mieux que ça !"
            }
        ]
    })


@website.route('/login', methods=['GET', 'POST'])
def login_page():
    form = SignInForm()
    return render_template('pages/formpage.html', theme='dark', user=False, form=form)


@website.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    return render_template('pages/formpage.html', theme='dark', user=False, form=form)

@website.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile_page():
    form = EditProfileForm()
    return render_template('pages/formpage.html', theme='dark', user={
        "is_chef": True,
        "is_admin": False,
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, form=form)


@website.route('/edit-recipe', methods=['GET', 'POST'])
def edit_recipe_page():
    return render_template('pages/edit-recipe.html', theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    })


@website.route('/profile', methods=['GET', 'POST'])
def profile_page():
    return render_template('pages/profile.html', theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, viewed_user={
        "pseudo": "MichelDupont24",
        "ranking": 4,
        "name": "Michel Dupont",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Michel_Cremades.jpg",
        "birthday": "15 février 1968",
        "is_chef": True,
        "is_admin": False,
        "nb_subscribers": 42,
        "current_user_is_subscribed": False,
        "recipes": [
            {
                "name": "Quiche namuroise",
                "average_rating": 4,
                "picture": "https://ds1.static.rtbf.be/article/image/1248x702/5/3/4/bc6fe82635b1429d3e886eec0fc34f49-1515748913.jpg",
                "url": "/light",
                "nb_favorites": 89,
                "current_user_favorited": True,
            },
            {
                "name": "Quiche namuroise v2",
                "average_rating": 4,
                "picture": "https://ds1.static.rtbf.be/article/image/1248x702/5/3/4/bc6fe82635b1429d3e886eec0fc34f49-1515748913.jpg",
                "url": "/light",
                "nb_favorites": 3,
                "current_user_favorited": False,
            },
            {
                "name": "Quiche namuroise v3",
                "picture": "https://ds1.static.rtbf.be/article/image/1248x702/5/3/4/bc6fe82635b1429d3e886eec0fc34f49-1515748913.jpg",
                "url": "/light",
                "nb_favorites": 17,
                "current_user_favorited": False,
                "average_rating": None
            },
            {
                "name": "Quiche namuroise v3 final",
                "picture": "https://ds1.static.rtbf.be/article/image/1248x702/5/3/4/bc6fe82635b1429d3e886eec0fc34f49-1515748913.jpg",
                "url": "/light",
                "nb_favorites": 1,
                "current_user_favorited": False,
                "average_rating": None
            },
            {
                "name": "Quiche namuroise final le vrai",
                "picture": "https://ds1.static.rtbf.be/article/image/1248x702/5/3/4/bc6fe82635b1429d3e886eec0fc34f49-1515748913.jpg",
                "url": "/light",
                "nb_favorites": 158,
                "current_user_favorited": True,
                "average_rating": 5
            }
        ]
    })

@website.route('/my-recipes')
def my_recipes_page():
    return render_template('pages/my-recipes.html', page='my-recipes', title="Mes recettes", theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    })

@website.route('/subscriptions')
def subscriptions_page():
    return render_template('pages/sorted.html', page='subscriptions', title="Abonnements", theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    })

@website.route('/favorites')
def favorites_page():
    return render_template('pages/sorted.html', page='favorites', theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, title="Recettes favorites")

@website.route('/search')
def search_page():
    return render_template('pages/sorted.html', theme='dark', user={
        "avatar_url": "https://rosieshouse.org/wp-content/uploads/2016/06/avatar-large-square.jpg"
    }, title="Résultat de la recherche")

# TODO add routes here with "website" instead of "app"
