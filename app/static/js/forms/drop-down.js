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
            
            console.log("focusout !");
        });

        // Disable main button click
        mainButton.on("click", function (e) {
            e.preventDefault();
        });


        // Keep track of the mouse position
        mainButton.on("mouseenter", function(e){
            buttonEntered = true;
            console.log("entered main button");
        })
        mainButton.on("mouseleave", function(e){
            buttonEntered = false;
            console.log("left main button");
            handleMouseLeave(e);
        })
        optionList.on("mouseenter", function(e){
            optionsEntered = true;
            console.log("entered options");
        })
        optionList.on("mouseleave", function(e){
            optionsEntered = false;
            console.log("left options");
            handleMouseLeave(e);
        })

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
