$(document).ready(function() {
    $.each($("tbody").children("tr"), function(row_ind, row) {
        let user_link = $($(row).find("a")[0]).attr("href").split('/')
        let user_id = parseInt(user_link[user_link.length - 1])
        let button = $(row).find(".dropdown-menu").find("button")[0]

        console.log(user_id, $(button).val())
        $(button).on("blur", function() {
            //on blur wait a few instants and send request
            setTimeout(function() {

                $.post("/api/user/update_role", { 'user_id': user_id, 'group_id': parseInt($(button).val()) }).done(function() {
                    console.log($(button).val())
                }).fail(function() {
                    let new_error = $("Could not update role").addClass("helper-text error")
                    $(button).after($(new_error))

                    setTimeout(function() {
                        $(button).parent().find(".error").remove()
                    }, 5000)
                })
            }, 200)
        })
    });
});