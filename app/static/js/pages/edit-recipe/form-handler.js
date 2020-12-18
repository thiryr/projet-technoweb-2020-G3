$(document).ready(function() {
    submit = $("form").find("button.filled-button")
    cancel = $("form").find("button.outlined-button")

    $(submit).on("click", function(e) {
        e.preventDefault();

        if ($(submit).attr("disabled") === true) {
            return;
        }

        var error_occured = false

        clear_errors()

        var title = get_title()
        var people = get_people()
        var diff = get_difficulty()
        var public = get_public()
        var tags = get_tags()
        var cat = get_category()
        var ingredients = get_ingredients()
        var utensils = get_utensils()
        var steps = get_steps()

        let image = get_image()


        if (!check_title(title)) {
            error_occured = true
            append_error("Veuillez n'utiliser que des lettres, des chiffres, des tirets ou des espaces.", $("#title"))
        }

        if (!check_people(people)) {
            error_occured = true
            append_error("Vous devez indiquer au moins une personne.", $("#nb-people"))
        }

        if (!check_difficulty(diff)) {
            error_occured = true
            append_error("Ce champ est obligatoire.", $("#diff3"))
        }


        if (!check_category(cat)) {
            error_occured = true
            append_error("Ce champ est obligatoire.", $("#category-input").find("button")[0])
        }

        if (!check_ingredients(ingredients)) {
            error_occured = true
            append_error("Veuillez au moins entrer une ligne.", $("#ingredients-input").find(".add-line"))
        }

        if (!check_utensils(utensils)) {
            error_occured = true
            append_error("Veuillez au moins entrer une ligne.", $("#utensils-input").find(".add-line"))
        }

        if (!check_ingredients(steps)) {
            error_occured = true
            append_error("Veuillez au moins entrer une ligne.", $("#steps-input").find(".add-line"))
        }

        if (image && !check_image(image)) {
            error_occured = true
            append_error("Seules les images JPG ou PNG sont autorisées.", $("#image-input"))
        }



        //if input-error
        if (error_occured) {
            append_error("Veuillez corriger le formulaire avant de soumettre.", $(submit))
        } else {

            $.ajax({
                    type: "POST",
                    url: "/api/recipe/new",
                    data: JSON.stringify({
                        'title': title,
                        'category': cat,
                        'people': people,
                        'difficulty': diff,
                        'public': public,
                        'ingredients': ingredients,
                        'utensils': utensils,
                        'steps': steps,
                        'tags': tags
                    }),
                    contentType: "application/json"
                }).done(function(r) {
                    let new_id = JSON.parse(r).new_id

                    if (image) {
                        let fd = new FormData()
                        fd.append('file', image)
                        fd.append('id', new_id)
                        $.ajax({
                            url: '/api/recipe/add_image',
                            type: 'post',
                            data: fd,
                            processData: false,
                            contentType: false,
                            success: function(response) {
                                window.location.href = `./recipe/${new_id}`
                            }
                        });
                    } else {
                        window.location.href = `./recipe/${new_id}`
                    }
                })
                .fail(function() {
                    //append error and disable for two seconds
                    append_error("An error occured when trying to submit your post, make sure all your inputs look fine and try again in a few seconds", $(submit))
                    $(submit).prop("disabled", true)
                    setTimeout(() => {
                        $(submit).prop("disabled", false)
                        clear_errors()
                    }, 2000)
                })


        }

    });

    $(cancel).on("click", function(e) {
        e.preventDefault();
    });
});


function get_title() {
    return $("#title").val()
}

//returns false if title is invalid
function check_title(title) {
    if (title === null)
        return false
    if (title == "")
        return false
            //regex for 'regular' string
    if (/^[a-zA-Z0-9- ]*$/.test(title) == false)
        return false

    return true
}


function get_people() {
    result = $("#nb-people").val()
    return parseInt(result)
}

function check_people(people) {
    if (people === null)
        return false
    if (people < 1)
        return false
    return true
}



function get_difficulty() {
    var diff = $('input[name="difficulty"]:checked').attr("id");
    if (diff === "diff1")
        return 1
    if (diff === "diff2")
        return 2
    if (diff === "diff3")
        return 3
    return 0
}

function check_difficulty(diff) {
    if (diff === null)
        return false
    if (diff < 1 || diff > 3)
        return false
    return true
}



function get_public() {
    return $('#public:checked').length > 0
}

function check_public() {
    return true
}



function get_tags() {
    var list_elements = $(".tag-input").children('div.field').children('ul').children('li')
    var values = $.map($(list_elements), function(list_element, ind) {
        //split to only retrieve the raw content without subdivs
        return $(list_element).html().split('<')[0]
    });

    return values
}

function check_tags() {
    return true
}






function get_drop_down_values(drop_down_id) {
    return $(`#${drop_down_id}`).children('div.field').children('button').val()
}

function get_category() {
    return get_drop_down_values("category-input")
}

function check_category(category) {
    if (category === null)
        return false
    if (category.trim() == "")
        return false
    return true
}





function get_image() {
    files = document.getElementById("image-input").files
    if (files.length < 1) {
        return null
    }
    return files[0]
}

function check_image(file) {
    const fileTypes = [
        "image/jpeg",
        "image/png"
    ];
    return fileTypes.includes(file.type)
}



function get_list_menu_values(menu_id) {
    var list_elements = $(`#${menu_id}`).children(".list").children("li")
    var values = $.map($(list_elements), function(list_element, ind) {
        return $(list_element).children(".field").children('input').val()
    });
    //remove the add-field
    values.pop()
    return values
}


function get_ingredients() {
    return get_list_menu_values("ingredients-input")
}

function get_utensils() {
    return get_list_menu_values("utensils-input")
}

function get_steps() {
    return get_list_menu_values("steps-input")

}

function check_ingredients(ingredients) {
    if (ingredients === null)
        return false
    if (ingredients.length < 1)
        return false
    return true
}

function check_utensils(utensils) {
    if (utensils === null)
        return false
    if (utensils.length < 1)
        return false
    return true
}

function check_steps(steps) {
    if (steps === null)
        return false
    if (steps.length < 1)
        return false
    return true
}


function append_error(error_str, toElement) {
    var new_error = $(`<p>${error_str}</p>`).addClass("helper-text error")
    $(toElement).parent().after($(new_error))
    $(toElement).addClass('error');
    $(toElement).parent().addClass('error');
    console.log(error_str)
}

function preppend_error(error_str, toElement) {
    var new_error = $(`<p>${error_str}</p>`).addClass("helper-text error")
    $(toElement).parent().before($(new_error))
}

function clear_error(fromElement) {
    $(fromElement).parent().nextAll(".helper-text.error").remove()
    $(fromElement).parent().prevAll(".helper-text.error").remove()
    $(fromElement).parent().find(".helper-text.error").remove()
}

function clear_errors() {
    clear_error($("#title"))
    clear_error($("#nb-people"))
    clear_error($("#category-input"))
    clear_error($("#ingredients-input"))
}