//get recipe id
var url = $(location).attr("href")
var url_path = url.split("/")
var recipe_id_str = url_path[url_path.length - 1]
var recipe_id = parseInt(recipe_id_str)



//switch visibility
$(document).ready(function() {

    $("#visibility").click(function() {
        //'public' is the value to be set
        $.post("/api/recipe/update_visibility", { 'recipe_id': recipe_id }).done(function(expected_json) {
                //remove or add lock, modify button
                expected_json = JSON.parse(expected_json)

                if (expected_json.public == false) {
                    $($(".info").children(".row")[0]).append('<i class="fa fa-lock margin-right"></i>')

                    $("#visibility").attr("value", "private")
                    $("#visibility").html("Rendre public")
                } else {
                    $(".info").find(".fa-lock").remove()

                    $("#visibility").attr("value", "public")
                    $("#visibility").html("Rendre privée")
                }

            })
            .fail(function() {

                //do nothing for now
            })

    });

    //detele

    $("#delete").click(function() {

        $.post("/api/recipe/remove", { 'recipe_id': recipe_id }).done(function(expected_json) {
                window.location.href = "/"
            })
            .fail(function() {
                //do nothing for now
            })

    });

    //pin


    const path_url = window.location.href.split('/')
    const id = path_url[path_url.length - 1].split('?')[0]

    let target_url = "/api/recipe/switch_pin"

    $("#pin").click(function() {
        //'public' is the value to be set
        $.post(target_url, { 'recipe_id': id }).done(function(expected_json) {
                //remove or add lock, modify button
                expected_json = JSON.parse(expected_json)
                if (expected_json.pinned == false) {
                    $("#pin").attr("value", "unpinned")
                    $("#pin").html("Épingler")
                } else {
                    $("#pin").attr("value", "pinned")
                    $("#pin").html("Désépingler")
                }


            })
            .fail(function() {

                //do nothing for now
            })

    });
})