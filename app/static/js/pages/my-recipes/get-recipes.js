jQuery(function() {

    retrieve_own_recipes()

});



function get_own_recipe_url(id) {
    return `../recipe/${id}`
}

function get_own_profile_url(id) {
    return `../profile/${id}`
}

function display_own_recipes(recipes_json) {
    recipes = recipes_json.recipes_info
    recipes.forEach(recipe => display_recipe(recipe, "#my-recipes-list"))
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