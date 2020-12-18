const sab = "S'abboner"
const desab = "Se desabonner"


const create_url = "../api/subscription/create"
const remove_url = "../api/subscription/remove"

$(document).ready(function() {
    const path_url = window.location.href.split('/')
    const id = path_url[path_url.length - 1].split('?')[0]

    let current_state = $("#subscribe-button").children("button").html()


    let target_url = current_state === sab ? remove_url : create_url

    $("#subscribe-button").children("button").on("click", function() {

        $.post(target_url, { 'id': id }).done(function() {
            current_state = (current_state === sab ? desab : sab)
            $("#subscribe-button").children("button").html(current_state)
            target_url = target_url === create_url ? remove_url : create_url
        })
    })

});