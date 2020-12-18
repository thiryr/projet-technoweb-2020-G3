/**
 * @file tag input logic
 */

jQuery(function () {


    $.each($(".tag-input"), function (ind, tag_input) {
        /** Whole tag input field */
        let tag_content = $(tag_input).children(".field");
        /** The list contained in the field  */
        let list = tag_content.children("ul");
        /* List of all the tags */
        let tag_list = list.children("li");
        /** The input field */
        let input_field = list.children("input");
        /** The backspace key is pressed */
        let backspace_down = false;

        /** 
         * Append to tag output
         * @returns true if added, false otherwide
         */
        function add_tag_from_input() {

            // Get value
            value = input_field.val().trim();

            if (value === "") {
                return false;
            }

            // Reset field
            input_field.val("");

            // Append tag
            $(`<li>${value} <button><i class='fa fa-times'></i></button></li>`).insertBefore(input_field);

            return true;
        }

        /** Handle key presses */
        input_field.on("keydown", function (e) {
            // Enter
            if (e.which === 13) {
                // Try to add, update if necessary
                if (add_tag_from_input()) {
                    update_event_handlers();
                }
            }
            // Backspace
            // Only count the first press (don't repeat)
            else if (e.which === 8 && !backspace_down) {
                backspace_down = true;
                if (input_field.val() == "" && tag_list.length > 0) {
                    input_field.prev().remove();
                }
            }
        });

        /** Reset backspace_down on key up */
        input_field.on("keyup", function (e) {
            if (e.which === 8) {
                backspace_down = false;
            }
        });

        /**
         * Update list and event functions
         */
        function update_event_handlers() {
            // Update li list
            tag_list = list.children("li");
            // Add click handler to delete
            $.each(tag_list, function (ind_update_event, list_item) {
                $(list_item).children("button").on("click", function () {
                    list_item.remove();
                });
            });
        }
    });
});