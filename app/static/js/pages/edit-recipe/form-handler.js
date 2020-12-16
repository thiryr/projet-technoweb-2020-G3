$(document).ready(function() {
    submit = $("form").find("button.filled-button")
    cancel = $("form").find("button.outlined-button")

    $(submit).on("click", function(e) {
        e.preventDefault();
    });

    $(cancel).on("click", function(e) {
        e.preventDefault();
    });
});


function get_title() {
    return $("#title").value()
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
    return $("#nb-people").value()
}

function check_people(people) {
    if (people === null)
        return false
    return true
}


function get_difficulty() {
    var diff = $('input[name="difficulty"]:checked').id();
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
    return true
}




function get_list_menu_values(menu_id) {
    var list_elements = $(`#${menu_id}`).children("ul.list").children("li")
    var values = $.map($(list_elements), function(list_element, ind) {
        return $(list_element).children("div.field").val()
    });

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