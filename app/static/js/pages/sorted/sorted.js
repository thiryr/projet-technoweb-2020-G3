function get_drop_down_values(drop_down_id) {
    return $(`#${drop_down_id}`).children('div.field').children('button').val()
}
//can be "recent" or "trending"
var current_sorting = "recent"

$(document).ready(function() {
    var sort_selector = $("#sort-input")
    var buttons = $(sort_selector).find("button")

    retrieve_recipes()

    $.each($(buttons), function(button_id, button) {
        $(button).on("click", function() {

            current_sorting = get_drop_down_values("sort-input")
            retrieve_recipes()


        });
    });
});


function retrieve_recipes() {
    $.get("/api/recipe/subscription_sorted", { 'sorting_mode': current_sorting }).done(function(r) {
        console.log(r)
    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $($("#sort-input").find(button)[0]).parent().before($(new_error))

        setTimeout(() => {
            $("#sort-input").find("p.helper-text error").remove()
        }, 2000)
    })

}