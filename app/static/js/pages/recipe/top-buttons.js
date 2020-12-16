//get recipe id
var url = $(location).attr("href")
var url_path = url.split("/")
var recipe_id_str = url_path[url_path.length - 1]
var recipe_id = parseInt(recipe_id_str)



//switch visibility
$(document).ready(function() {

    //BIG ASSUMPTION
    //Recipe public if no lock icon, LOCK ICON SHOULD ONLY BE USED FOR THAT ON THIS PAGE
    var is_public = $(".info").find(".fa-lock").length == 0
    $("#make-public").click(function() {
        //'public' is the value to be set
        $.post("/api/recipe/switch_visibility", { 'recipe_id': recipe_id, 'public': !is_public }).done(function(expected_json) {
                //remove or add lock
                if (expected_json.public == false)
                    $(".info").find(".fa-lock").remove()
                else
                    $($(".info").children(".row")[0]).append('<i class="fa fa-lock margin-right"></i>')

                is_public = expected_json.public

            })
            .fail(function() {

                //do nothing for now
            })

    });
})

//detele
$(document).ready(function() {

    $("#delete").click(function() {

        $.post("/api/recipe/remove", { 'recipe_id': recipe_id }).done(function(expected_json) {
                location.href = "../index"
            })
            .fail(function() {
                //do nothing for now
            })

    });
})

//TODO pin