//disable default redirects for forms
$(document).ready(function() {


    $(document).on('keypress', function(e) {
        if (e.which == 13)
            e.preventDefault();
    })
});