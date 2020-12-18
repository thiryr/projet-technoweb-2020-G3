jQuery(function() {
    retrieve_recommended_recipes()

});


function retrieve_recommended_recipes() {
    $.get('/api/recipe/get_recommendation').done(function(recipes) {
        //display them
        console.log(recipes)
        $("#recommended-list").find(".recipe").remove();

        display_recipes(JSON.parse(recipes), "#recommended-list");

    }).fail(function() {
        let new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error");
        $("#recommended-list").append($(new_error));
    })
}