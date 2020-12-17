$(document).ready(function() {


    $.each($(".input-list"), function(ind, input_list) {
        var list = $(input_list).children(".list")
            //set the first add_field
        var fields_li = $(list).children("li")
        var add_field_li = null
        $.each($(fields_li), function(indexInArray, field_li) {
            if ($(field_li).children(".field").hasClass("add-line")) {
                add_field_li = $(field_li)
                return false
            }
        });
        var add_field = add_field_li.children(".field")

        function set_line_events() {
            //sets an event on all fields when empty
            $.each($(list).find("li"), function(ind_input, li) {
                //unless add-line
                var field = $(li).children(".field")
                if (!$(field).hasClass("add-line")) {
                    var input = $(field).children("input")
                        //remove previously binded event
                    $(input).off("focusout")
                        //add event to remove unused
                    $(input).on("focusout", () => {
                        if ($(input).val().trim() === "") {
                            $(li).remove()
                        }
                    })

                    // add event to add a new element
                    $(input).on("keypress", function(e) {
                        if (e.which == 13) {
                            $(add_field).children("input").focus()
                        }
                    })
                }
            });

        }

        set_line_events()

        set_new_line_event()

        function set_new_line_event() {
            $(add_field).on("keyup", function() {
                //do nothing if input was not registered
                if ($(add_field).children("input").val().trim() !== "") {
                    //clone structure
                    new_field_li = $(add_field_li).clone()
                    new_field = $(new_field_li).children(".field")

                    $(new_field).children("input").val("")

                    //append structure
                    $(list).append($(new_field_li))

                    //remove special features
                    $(add_field).removeClass("add-line")
                    $(add_field).find("svg").remove()

                    $(add_field).off("keyup")

                    //update field
                    add_field_li = $(new_field_li)
                    add_field = $(new_field)

                    //make sure every field has the remove event
                    set_line_events()

                    //set an event to make a new add-field when this one gets overriden
                    set_new_line_event()


                }

            });
        }
    });
});


//not my cleanest work


/*
get values with
    var list_elements = $("#ingredients-input").children("ul.list").children("li")
    var values = $.map($(list_elements), function(list_element, ind) {
        return $(list_element).children("div.field").val()
    });
*/