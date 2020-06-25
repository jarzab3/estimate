function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function highlight_input_code() {
    let enter_input = $('input#enter-input-code');
    let code = enter_input.val();
    if (code.length === 5) {
        enter_input.css("color", "red");
    }
}

function check_code(request_data) {
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: "api/enter_session",
        data: request_data,
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        success: function (data, status, xhr) {
            if (data.code != null) {
                window.location = '/session/' + data.code;
            } else {
                highlight_input_code();
            }
        },
        error: function (xhr, status, error) {
            console.log("Error while editing consent date: " + error);
        },
    });
}

$(document).ready(function () {

    let enter_input = $('input#enter-input-code');
    enter_input.on("input", function () {
        let code = this.value;
        if (code.length === 5) {
            let request_data = JSON.stringify({code: code});
            check_code(request_data);
        }
        if (code.length < 5) {
            enter_input.css("color", "#465b71");
        }
    });

    setTimeout(function () {
        $('#enter-input-code').focus()
    }, 2000);

    let enter_modal = $("#enter-room-button");
    enter_modal.on("click", function () {
        enter_input.val("");
    })

});



