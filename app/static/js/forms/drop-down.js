jQuery(function () {

    $.each($(".dropdown-menu"), function (ind, menu) {
        /** Main button */
        let mainButton = $(menu).children(".field").children("button");
        /** Options */
        let optionList = $(menu).children(".options");
        let options = optionList.find("button");

        // Keep track of the mouse position
        let buttonEntered = false;
        let optionsEntered = false;
        let mainFocused = false;

        // Open on focus
        mainButton.on("focus", function () {
            mainFocused = true;
            $(menu).children(".options").addClass("opened");
        });

        // Close on lose focus
        mainButton.on("blur", function (e) {
            mainFocused = false;
            $(menu).children(".options").removeClass("opened");
        });

        // Disable main button click
        mainButton.on("click", function (e) {
            e.preventDefault();
        });


        // Keep track of the mouse position
        mainButton.on("mouseenter", function(e){
            buttonEntered = true;
        })
        mainButton.on("mouseleave", function(e){
            buttonEntered = false;
            handleMouseLeave(e);
        })
        optionList.on("mouseenter", function(e){
            optionsEntered = true;
        })
        optionList.on("mouseleave", function(e){
            optionsEntered = false;
            handleMouseLeave(e);
        })
        /** Close the dropdown if the mouse left both regions after some time */
        function handleMouseLeave(e) {
            setTimeout(function() {
                if (mainFocused && !buttonEntered && !optionsEntered) {
                    mainButton.trigger("blur");
                }
            }, 5);
        }

        $.each(options, function (i, option) {
            $(option).on("click", function (e) {
                // Don't reload page
                e.preventDefault();

                // Update main button
                mainButton.children("span").removeClass("placeholder");
                mainButton.children("span").text($(option).text());
                mainButton.val($(option).val());

                // Deselect every option
                $.each(options, function (i, optionToDeselect) {
                    $(optionToDeselect).removeClass("selected");
                });

                // Select the clicked option
                $(option).addClass("selected");
            });
        });

    });
});
