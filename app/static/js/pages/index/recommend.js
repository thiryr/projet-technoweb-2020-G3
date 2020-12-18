$(document).ready(function() {

    retrieve_recommended_recipes()

});



function get_recommended_recipe_url(id) {
    return `../recipe/${id}`
}

function get_recommended_profile_url(id) {
    return `../profile/${id}`
}



function display_recommended_recipe(recipe) {
    let recipe_element = recipeThumbnail(
        recipe.recipe_name,
        recipe.author_id,
        recipe.img_url,
        recipe.favorites,
        recipe.is_favorite,
        displayName(recipe.author_nick, recipe.author_first, recipe.author_last), 
        recipe.author_id, 
        recipe.author_chef,
        recipe.average_rating
    )

    $("#recommended-list").append(recipe_element)

}

function display_recommended_recipes(recipes_json) {
    recipes = recipes_json.recipes_info
    recipes.forEach(recipe => display_recommended_recipe(recipe))
}

function retrieve_recommended_recipes() {
    $.get('/api/recipe/get_recommendation').done(function(recipes) {
        //display them

        $("#recommended-list").find(".recipe").remove()

        display_recommended_recipes(JSON.parse(recipes))

    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $("#recommended-list").append($(new_error))
    })
}