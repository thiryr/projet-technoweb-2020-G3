$(document).ready(function() {


    $.each($(".tag-input"), function(ind, tag_input) {
        var tag_content = $(tag_input).children(".field")

        var list = $(tag_content).children("ul")

        var list_items = $(list).children("li")
        var input_field = $(list).children("input")

        console.log()


        //append to this tag-input
        function add_tag_from_input() {
            //get value
            value = $(input_field).val()
                //reset field
            $(input_field).val("")
                //append tag
            $(list).append(`<li>${value} <button><i class='fa fa-times'></i></button></li>`)
        }


        $(input_field).on("keypress", function(e) {
            if (e.which == 13) {
                add_tag_from_input()
                update_event_handlers()
            }
        });


        function update_event_handlers() {
            //update li list
            list_items = $(list).children("li")
                //add click handler to delete
            $.each(list_items, function(ind_update_event, list_item) {
                $(list_item).children("button").on("click", function() {
                    $(list_item).remove()
                });
            });
        }
    });
});