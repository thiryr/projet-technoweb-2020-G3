jQuery(function() {
    starting_popular_number = 20
    retrieve_recipes()

    $("#more-trending").on("click", function() {
        starting_popular_number += 10
        retrieve_recipes()
    })
});



function get_recipe_url(id) {
    return `../recipe/${id}`
}

function get_profile_url(id) {
    return `../profile/${id}`
}



function display_recipe(recipe) {
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


    $("#trending-list").append(recipe_element)

}

function display_recipes(recipes_json) {
    recipes = recipes_json.recipes_info
    recipes.forEach(recipe => display_recipe(recipe))
}

function retrieve_recipes() {

    $.get('/api/recipe/get_popular', { 'number': starting_popular_number }).done(function(recipes) {
        //display them

        $("#trending-list").find(".recipe").remove()

        let json_info = JSON.parse(recipes)

        display_recipes(json_info)

        //remove button if at the end
        if (json_info.recipes_info.length < starting_popular_number) {
            $("#more-trending").remove()
        }

    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $("#trending-list").append($(new_error))

    })
}