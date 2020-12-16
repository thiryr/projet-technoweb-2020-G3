//disable default redirects for forms and buttons
$(document).ready(function() {


    $(document).on('keypress', function(e) {
        if (e.which == 13)
            e.preventDefault();
    })
    $(document).on('click', function(e) {
        if (e.which == 13)
            e.preventDefault();
    })
});