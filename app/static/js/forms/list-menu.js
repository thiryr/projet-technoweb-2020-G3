$(document).ready(function() {
    $.each($(".list"), function(ind, list) {
        var list_fields = $(list).children("input")

        $.each(list_fields, function(indexInArray, field) {
            $(field).children("")

        });
    });
});