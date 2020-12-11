"""
This file contains the definition of the "frontend" blueprint containing
all the routes related to the frontend (pages).
"""

from app.models.recipe import Recipe
from flask import Blueprint, render_template

# Create blueprint
website = Blueprint('frontend', __name__, url_prefix='/')


@website.route('/')
def index_page():
    """
    Page d'accueil
    """
    return render_template('pages/recipe.html', theme='dark', user=True, is_chef=True, already_rated=False, recipe={
        "title": "Steak-frite",
        "author_name": "Mamy Dupont",
        "author_url": "/light",
        "average_rating": 3,
        "fav_count": 45,
        "current_user_favorited": True,
        "ingredients" : [
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
    })


@website.route('/light')
def index_page_light():
    return render_template('pages/recipe.html', theme='light', user=True)




@website.route('/login')
def login():
    return '<h1>Sign in now !</h1>'

# TODO add routes here with "website" instead of "app"
