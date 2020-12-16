$(document).ready(function() {

    $.each($(".dropdown-menu"), function(ind, menu) {
        var button = $(menu).children(".field").children("button")
        var fields = $(menu).children(".options").find("button")

        var hovered_field_nb = 0
        var has_been_entered = false


        $(button).mouseenter(function() {
            $(menu).children(".options").addClass("opened")
        });



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

            $(field).click(function() {
                $(button).children("span").val(`${$(field).val()}`)

                $.each(fields, function(clear_index, cleared_field) {
                    $(cleared_field).removeClass("selected")
                });

                $(field).addClass("selected")

            });
        });

    });
});