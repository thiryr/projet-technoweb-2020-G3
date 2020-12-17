$(document).ready(function() {

    //disable default redirects for forms
    $(document).on('keypress', function(e) {
        if (e.which == 13)
            e.preventDefault();
    })


    //like/dislike
    $("body").on("click", ".fa-heart", function(e) {
        e.preventDefault();


        var heart = $(e.target)
        var container = $(heart).parent()

        //if we land on the svg
        if ($(container).is("svg")) {
            heart = $(container)
            container = $(container).parent()
        }
        var counter = $(container).parent().children("span")
        if ($(container).is("button")) {


            var recipe_url = $(container).parent().parent().parent().children("a").attr("href")
            var recipe_url_path = recipe_url.split("/")
            var recipe_id = parseInt(recipe_url_path[recipe_url_path.length - 1])

            $.post("/api/favorite/switch", { 'recipe_id': recipe_id }).done(function(r) {
                //get response
                var new_state = JSON.parse(r).is_favorite

                //switch
                if (new_state === true && $(heart).attr("data-prefix") === "far") {
                    $(heart).attr("data-prefix", "fa")
                    $(counter).html(`${parseInt($(counter).html())+1}`)

                } else if (new_state === false && $(heart).attr("data-prefix") === "fa") {
                    $(heart).attr("data-prefix", "far")
                    $(counter).html(`${parseInt($(counter).html())-1}`)
                }
            }).fail(function() {
                //do nothing for now
            })
        }
    })
})