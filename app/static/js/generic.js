jQuery(function () {

    //disable default redirects for forms
    $("input").not(".searchbar").on('keypress', function (e) {
        if (e.which == 13) {
            // e.preventDefault();
        }
    })


    //like/dislike
    $("body").on("click", ".fa-heart", function (e) {
        e.preventDefault();


        var heart = $(e.target);
        var container = $(heart).parent();

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

            $.post("/api/favorite/switch", { 'recipe_id': recipe_id }).done(function (r) {
                //get response
                var new_state = JSON.parse(r).is_favorite

                //switch
                if (new_state === true && $(heart).attr("data-prefix") === "far") {
                    $(heart).attr("data-prefix", "fa")
                    $(counter).html(`${parseInt($(counter).html()) + 1}`)

                    console.log("added")

                } else if (new_state === false && $(heart).attr("data-prefix") === "fa") {
                    $(heart).attr("data-prefix", "far")
                    $(counter).html(`${parseInt($(counter).html()) - 1}`)
                    console.log("removed")
                }
            }).fail(function () {
                //do nothing for now
            })
        }
    })

    //link submit buttons
    $.each($("a"), function (ind, link) {
        if ($(link).attr("type") && $(link).attr("type") === "submit") {
            $(link).removeAttr("href");

            $(link).on("click", function () {
                $("form").trigger("submit");
            });
        }
    });

    //link profile, theme and disconnect buttons
    $("#theme-switch-button").on("click", function () {
        $.post("/api/theme/switch").done(function () {
            window.location.href = window.location.href
        })
    })
})

function recipeThumbnail(name, url, picture, nb_favorites, current_user_favorited = false, author_name = "", author_id = 0, author_is_chef = false, average_rating = null) {
    // Create rating html
    let rating_html = "<div class=\"expand\">";
    if (average_rating !== null) {
        rating_html = "<ul class=\"rating expand\">";
        for (let i = 0; i < 5; i++) {
            if (i < average_rating) {
                rating_html += "<li><i class=\"fa fa-star\"></i></li>";
            }
            else {
                rating_html += "<li><i class=\"far fa-star\"></i></li>";
            }
        }
        rating_html += "</ul>";
    }

    // Create main element
    let element = $(`<div class=\"recipe\">
        <img src="${picture}" alt="${name}">
        <a class="name" href="/recipe/${url}">${name}</a>

        <div class="row all-width">
            <a class="author expand" href="/profile/${author_id}">${author_name}</a>
            ${author_is_chef ? '<span class="badge">Chef</span>' : ''}
        </div>
        <div class="row all-width">
            ${rating_html}
            <div class="fav-number">
                <span>${nb_favorites}</span>
                ${ isConnected() ? `<button><i class="${current_user_favorited ? 'fa' : 'far'} fa-heart"></i></button>` 
                : "<i class=\"far fa-heart\"></i>"}
            </div>
        </div>
    </div>`);

    return element;
}

function displayName(pseudo, firstName, lastName) {
    var username = '';
    if (!firstName && !lastName) {
        username = pseudo;
    } else {
        if (firstName)
            username += firstName;
        if (firstName && lastName)
            username += ' ';
        if (lastName)
            username += lastName;
    }
    return username;
}

function isConnected() {
    return $("body").attr('value') === 'connected';
}

function display_recipe(recipe, destination_id) {
    let recipe_element = recipeThumbnail(
        recipe.recipe_name,
        recipe.author_id,
        recipe.img_url,
        recipe.favorites,
        recipe.is_favorite,
        displayName(recipe.author_nick, recipe.author_first, recipe.author_last), 
        recipe.author_id, 
        recipe.author_chef,
        recipe.average_rating
    )

    $(destination_id).append(recipe_element)
}

function display_recipes(recipes_json, target_id) {
    recipes = recipes_json.recipes_info
    recipes.forEach(recipe => display_recipe(recipe, target_id))
}

function get_recipe_url(id) {
    return `../recipe/${id}`
}

function get_profile_url(id) {
    return `../profile/${id}`
}
