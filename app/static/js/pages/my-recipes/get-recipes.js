$(document).ready(function() {

    retrieve_own_recipes()

});



function get_own_recipe_url(id) {
    return `../recipe/${id}`
}

function get_own_profile_url(id) {
    return `../profile/${id}`
}


function get_own_recipe_element(img_url, recipe_id, recipe_name, author_id, author_nick, author_first, author_last, is_chef, rating, fav_number, is_fav) {

    var chef_badge = '<span class="badge">Chef</span>\n'
    if (!is_chef)
        chef_badge = ''

    var full_star = '<li><i class="fa fa-star"></i></li>\n'
    var empty_star = '<li><i class="far fa-star"></i></li>\n'

    var full_stars = ''
    var empty_stars = ''

    if (rating > 0) {
        for (var i = 0; i < 5; i++) {
            if (i < rating)
                full_stars += full_star
            else
                empty_stars += empty_star
        }
    }

    var heart = ''
    var full_heart = '<button><i class="fa fa-heart"></i></button>\n'
    var empty_heart = '<button><i class="far fa-heart"></i></button>\n'
    if (is_fav)
        heart = full_heart
    else
        heart = empty_heart

    var recipe_url = get_own_recipe_url(recipe_id)
    var profile_url = get_own_profile_url(author_id)

    var username = ''
    if (!author_first && !author_last) {
        username = author_nick
    } else {
        if (author_first)
            username += author_first
        if (author_first && author_last)
            username += ' '
        if (author_last)
            username += author_last
    }

    return `<div class="recipe">
    <img src="${img_url}"
        alt="${recipe_name}">
    <a class="name" href="${recipe_url}">${recipe_name}</a>

    <div class="row all-width">
        <a class="author expand" href="${profile_url}">${username}</a>
        ${chef_badge}
    </div>
    <div class="row all-width">
        <ul class="rating expand">
            ${full_stars}
            ${empty_stars}
        </ul>
        <div class="fav-number">
            <span>${fav_number}</span>
            ${heart}
        </div>
    </div>
</div>`
}


function display_own_recipe(recipe) {
    var filled_template = get_own_recipe_element(recipe.img_url, recipe.recipe_id, recipe.recipe_name, recipe.author_id,
        recipe.author_nick, recipe.author_first, recipe.author_last, recipe.author_chef,
        recipe.average_rating, recipe.favorites, recipe.is_favorite)

    $("#my-recipes-list").append($(filled_template))

}

function display_own_recipes(recipes_json) {
    recipes = recipes_json.recipes_info
    recipes.forEach(recipe => display_own_recipe(recipe))
}

function retrieve_own_recipes() {


    $.get('/api/recipe/user_recipes').done(function(recipes) {
        //display them

        $("#my-recipes-list").find(".recipe").remove()

        display_own_recipes(JSON.parse(recipes))

    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $("#my-recipes-list").append($(new_error))
    })
}