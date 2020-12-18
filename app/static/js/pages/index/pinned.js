$(document).ready(function() {

    retrieve_pinned_recipes()

});



function get_pinned_recipe_url(id) {
    return `../recipe/${id}`
}

function get_pinned_profile_url(id) {
    return `../profile/${id}`
}



function retrieve_pinned_recipes() {


    $.get('/api/recipe/get_pinned').done(function(recipes) {
        //display them

        $("#featured-list").find(".recipe").remove()

        display_recipes(JSON.parse(recipes), "#featured-list")

    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $("#featured-list").append($(new_error))
    })
}