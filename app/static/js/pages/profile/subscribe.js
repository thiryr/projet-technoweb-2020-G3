const sab = "S'abonner"
const desab = "Abonné"


const create_url = "/api/subscription/create"
const remove_url = "/api/subscription/remove"

jQuery(function() {
    const path_url = window.location.href.split('/');
    const id = path_url[path_url.length - 1].split('?')[0];

    let current_state = $("#subscribe-button").children("button").html().trim();
    let target_url = current_state === sab ? create_url : remove_url;

    $("#subscribe-button").children("button").on("click", function() {

        $.post(target_url, { 'id': id }).done(function() {

            // Toggle state
            current_state = (current_state === sab ? desab : sab);

            // Swap classes
            if (current_state === sab) {
                $("#subscribe-button").removeClass('subscribed');
                target_url = remove_url
            } else {
                $("#subscribe-button").addClass('subscribed');
                target_url = create_url;
            }

            // Update text
            $("#subscribe-button").children("button").html(current_state);
        })
    })

});