$(document).ready(function() {

    $.each($(".dropdown-menu"), function(ind, menu) {
        var button = $(menu).children(".field").children("button")
        var fields = $(menu).children(".options").find("button")

        var hovered_field_nb = 0
        var has_been_entered = false

        //open on hover
        $(button).mouseenter(function() {
            $(menu).children(".options").addClass("opened")
        });

        //close on click
        $('html').click(function(e) {
            $(menu).children(".options").removeClass("opened");
        });

        //disable main button click
        $(button).on("click", function(e) {
            e.preventDefault();
        })



        $.each(fields, function(field_index, field) {

            //add a field
            $(field).mouseenter(function(e) {
                hovered_field_nb += 1
                has_been_entered = true

            });

            //if no field has been entered, close after 0.005 seconds
            $(field).mouseout(function(e) {
                hovered_field_nb -= 1

                setTimeout(() => {
                    if (hovered_field_nb === 0) {
                        $(menu).children(".options").removeClass("opened")
                        has_been_entered = false
                        hovered_field_nb = 0
                    }
                }, 5)

            });

            $(field).on("click", function(e) {
                e.preventDefault();

                $(button).children("span").html(`${$(field).html()}`)
                $(button).val(`${$(field).val()}`)

                $.each(fields, function(clear_index, cleared_field) {
                    $(cleared_field).removeClass("selected")
                });

                $(field).addClass("selected")

                //close on select
                $(menu).children(".options").removeClass("opened")
                has_been_entered = false
                    //has to be set to 1, likely because the mouse doesn't "leave" the field
                hovered_field_nb = 1
            });
        });

    });
});


/*
get value through

$(`#${drop_down_id}`).children('div.field').children('button').val()
*/