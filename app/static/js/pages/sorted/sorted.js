//can be "recent" or "trending"
var current_sorting = "recent"

jQuery(function() {
    var sort_selector = $("#sort-input")
    var buttons = $(sort_selector).find("button")

    retrieve_sorted_recipes()

    $.each($(buttons), function(button_id, button) {
        $(button).on("click", function() {

            current_sorting = get_drop_down_values("sort-input")
            retrieve_sorted_recipes()


        });
    });
});


function retrieve_sorted_recipes() {

    var current_url = window.location.href
    var current_url_path = current_url.split('/')
    var current_url_end = current_url_path[current_url_path.length - 1]
    var current_url_no_args = current_url_end.split('?')[0]

    var search_term = ''
    var target_url = ''

    if (current_url_no_args === 'subscriptions') {

        target_url = '/api/recipe/subscription_sorted'

    } else if (current_url_no_args === 'favorites') {

        target_url = '/api/recipe/favorites_sorted'

    } else if (current_url_no_args === 'search') {

        target_url = '/api/recipe/search_sorted'
        search_term = current_url_end.split('?')[1].split('=')[1]

    } else {

        console.log('unknown page, will not fetch')
        return;

    }

    console.log(target_url)

    $.get(target_url, { 'sorting_mode': current_sorting, 'search_term': search_term }).done(function(recipes) {
        //display them

        $("#sorted-list").find(".recipe").remove()

        display_recipes(JSON.parse(recipes), "#sorted-list")

    }).fail(function() {
        var new_error = $('<p>there was an issue, try again in a few seconds</p>').addClass("helper-text error")
        $($("#sort-input").find("button")[0]).parent().before($(new_error))

        setTimeout(() => {
            $("html").find(".helper-text.error").remove()
        }, 2000)

    })
}

function get_drop_down_values(drop_down_id) {
    return $(`#${drop_down_id}`).children('div.field').children('button').val()
}