jQuery(function () {
    starting_popular_number = 20
    retrieve_popular_recipes(starting_popular_number)

    $("#more-trending").on("click", function () {
        starting_popular_number += 10
        retrieve_popular_recipes(starting_popular_number)
    })
});


function retrieve_popular_recipes(starting_popular_number) {

    $.get('/api/recipe/get_popular', { 'number': starting_popular_number }).done(function (recipes) {
        //display them

        $("#trending-list").find(".recipe").remove()

        let json_info = JSON.parse(recipes)

        display_recipes(json_info, "#trending-list")

        //remove button if at the end
        if (json_info.recipes_info.length < starting_popular_number) {
            $("#more-trending").remove()
        }

    }).fail(function () {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $("#trending-list").append($(new_error))

    })
}