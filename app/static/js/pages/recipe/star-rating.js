//STAR-RATING
var current_rating = 0

$(window).on("load", function() {


    var rating_input = $("#rating-input")
        //retrieve the stars
    var list_elements = $(rating_input).children('li')
    var star_buttons = $.map($(list_elements), function(li, ind1) {
        return $(li).children('button')
    });

    //clear stars when user leaves rating input
    $(rating_input).mouseleave(function() {

        var stars = get_staricons(star_buttons)

        //set to current rating
        $(stars).each(function(index, star) {

            if (index < current_rating)
                $(star).attr('data-prefix', 'fa');
            else
                $(star).attr('data-prefix', 'far');
        });
    });

    //for each star symbol
    $.each(star_buttons, function(ind_h, hovered_button) {

        //select the score
        $(hovered_button).on("mouseenter", () => {

            var stars = get_staricons(star_buttons)

            //set all to empty when moving to another star
            $(stars).each(function(reset_index, star) {
                if (reset_index > ind_h && $(star).attr('data-prefix') === 'fa')
                    $(star).attr('data-prefix', 'far');
            });

            stars = get_staricons(star_buttons)
                //set the right ones to full
            $(stars).each(function(fill_index, star) {

                if ($(star).attr('data-prefix') === 'far') {
                    $(star).attr('data-prefix', 'fa');
                }
                //break out when reached last star
                if (ind_h === fill_index) {
                    return false
                }
            });

        });


        //click to set the score
        $(hovered_button).on("click", function(e) {
            current_rating = ind_h + 1

            //unlock the submit button
            if (submit_button_disabled)
                if (check_text())
                    switch_submit_button_state(false)
        });

    });


});


function staricon_from_button(button) {
    return $(button).children('svg')
}

function get_staricons(buttons) {
    return $.map(buttons, staricon_from_button)
}


//TEXT INPUT

$(document).ready(function() {
    $('#comment-input').keypress(function(e) {
        //unlock submit if ok on input
        if (submit_button_disabled)
            if (check_star_rating())
                switch_submit_button_state(false)
    });
});


//ERRORS

var rating_submit_errors = []

function add_rating_error(error_string) {
    rating_submit_errors.push(error_string)
}

function clear_error_display() {
    var error_messages = $('.comment.row.editor').find('.helper-text.error')

    $.each(error_messages, function(ind, error_message) {
        $(error_message).remove()
    });

}

function display_rating_errors() {

    rating_submit_errors.forEach(error_str => {
        new_error = $(`<p>${error_str}</p>`).addClass("helper-text error")
        $(".comment.row.editor").find('.column.bubble').append(new_error);
    });
    //reset errors
    rating_submit_errors = []
}

//SEND

var submit_button_disabled = false

function switch_submit_button_state(disabled) {
    submit_button_disabled = disabled
    $("#submit-rating-button").attr("disabled", submit_button_disabled)

    //clear display if can submit again
    if (!submit_button_disabled)
        clear_error_display()
}

$(document).ready(function() {
    //set button to default state
    switch_submit_button_state(submit_button_disabled)

    $("#submit-rating-button").click(function() {

        clear_error_display()

        if (check_star_rating()) {
            if (check_text()) {

                var url = $(location).attr("href")
                var url_path = url.split("/")
                var recipe_id_str = url_path[url_path.length - 1]
                var recipe_id = parseInt(recipe_id_str)


                $.post("/api/ratings/add", { 'recipe_id': recipe_id, 'score': current_rating, 'comment': $("#comment-input").val().trim() }).done(function() {
                        //if success, remove button, lock input and write success    
                        $("#comment-input").remove()
                        $("#comment-input").attr("readonly", "true")
                        new_message = $(`<p>Succesfully submited</p>`)
                        $(".comment.row.editor").find('.column.bubble').append(new_message);
                    })
                    .fail(function() {
                        add_rating_error("An error occured when trying to submit your post")
                        display_rating_errors()
                    })

                return;
            }
        }
        add_rating_error("You need to set a stars and a comment")
        display_rating_errors()
        switch_submit_button_state(true)
    });

});


function send_rating_return(response) {
    console.log(response)
}

//CHECK INPUT

function check_star_rating() {

    if (current_rating < 1 || current_rating > 5) {
        return false;
    }

    return true;

}

function check_text() {
    if ($('#comment-input').val().trim() === "") {
        return false
    }
    return true
}