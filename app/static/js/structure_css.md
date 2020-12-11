# Expected CSS structures

Fichier temporaire à destination des gens qui font le js

## Recipe thumbnail

Thumbnail de recette :

```html
<div class="recipe">
    <img src="IMAGE_URL"
        alt="RECIPE_NAME">
    <a class="name" href="RECIPE_URL">RECIPE_NAME</a>
    <a class="author" href="PROFILE_URL">AUTHOR_NAME</a>
    <div class="row all-width">
        <ul class="rating expand">
            <li><i class="fa fa-star"></i></li>
            <li><i class="fa fa-star"></i></li>
            <li><i class="fa fa-star"></i></li>
            <li><i class="far fa-star"></i></li>
            <li><i class="far fa-star"></i></li>
        </ul>
        <div class="fav-number">
            <span>FAVORITE_NUMBER</span>
            <button><i class="far fa-heart"></i></button>
        </div>
    </div>
</div>
```

Obligatoire :
- image: (remplacer `IMAGE_URL` et `RECIPE_NAME`)
- nom: (remplacer `RECIPE_NAME` et `RECIPE_URL`)
- auteur: (remplacer `AUTHOR_NAME` et `PROFILE_URL`)
- nombre de favoris (remplacer `FAVORITE_NUMBER`).
  - Si l'utilisateur a déjà ajouté la recette en favoris, remplacer `far fa-heart` par `fa fa-heart`

Facultatif:
- Rating
  - Il faut 5 li avec des étoiles. 
  - les `fa fa-star` sont pleines et jaunes, les `far fa-star` sont vides. Il faut donc mettre autant de `fa fa-star` que le rating, puis le reste en `far fa-star`.
  - S'il n'y a aucun rating pour cette recette, remplacer tout le bloc `<ul class="rating expand">...</ul>` par un bloc vide `<div class="expand"></div>`

## Commentaire

Commentaire de chef:

```html
<li class="comment row">
    <img class="avatar" src="AVATAR_URL" alt="avatar">
    <div class="column bubble">
        <div class="row all-width">
            <span class="name expand">USER_NAME</span>
            <ul class="rating">
                <li><i class="fa fa-star"></i></li>
                <li><i class="fa fa-star"></i></li>
                <li><i class="fa fa-star"></i></li>
                <li><i class="far fa-star"></i></li>
                <li><i class="far fa-star"></i></li>
            </ul>
        </div>
        <span class="message">MESSAGE</span>
    </div>
</li>
```

Remplacer:
- ``AVATAR_URL`` par l'url de l'avatar du chef
- `USER_NAME` par le nom du chef (prénom /nom, pseudo ?)
- Remplacer l'intérieur de rating pour indiquer le rating sélectionné (même principe qu'au dessus avec les `fa` remplis et les `far` vides)
- Remplacer `MESSAGE` par le message