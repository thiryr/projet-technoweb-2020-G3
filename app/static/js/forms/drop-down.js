drop_down_values = []

$(document).ready(function() {

    $.each($(".dropdown-menu"), function(ind, menu) {
        var button = $(menu).children(".field").children("button")
        var fields = $(menu).children(".options").children("button")


        $(button).mouseover(function() {
            $(menu).children(".options").addClass("opened")
            display_options(fields)
        });

        $(menu).mouseout(function() {
            $(menu).children(".options").removeClass("opened")
        })


        $.each(fields, function(field_index, field) {
            $(field).click(function() {
                $(button).children("span").val(`${$(field).val()}`)

                $.each(fields, function(clear_index, cleared_field) {
                    $(cleared_field).removeClass("selected")
                });

                $(field).addClass("selected")

            });
        });

        function display_options(field_list) {

        }
    });
});