$(window).on("load", function() {

    var current_rating = 0


    var rating_input = $("#rating-input")
        //retrieve the stars
    var star_buttons = $(rating_input).children('li').find('button')

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


        $(hovered_button).mouseenter(function() {

            var stars = get_staricons(star_buttons)

            //set all to empty when moving to another star
            $(stars).each(function(index, star) {
                $(star).attr('data-prefix', 'far');
            });

            //set the right ones to full
            $(stars).each(function(index, star) {
                if ($(star).attr('data-prefix') === 'far') {
                    $(star).attr('data-prefix', 'fa');
                }
                //break out when reached last star
                if (ind_h === index)
                    return false
            });

        });

        $(hovered_button).click(function() {
            current_rating = ind_h + 1
        });

    });


});


function staricon_from_button(button) {
    return $(button).children('svg')
}

function get_staricons(buttons) {
    return $.map(buttons, staricon_from_button)
}


/*
if ($(star).attr('data-prefix') === "far") {
    $(star).attr('data-prefix', 'fa');
} else {
    $(star).attr('data-prefix', 'far');
}
*/