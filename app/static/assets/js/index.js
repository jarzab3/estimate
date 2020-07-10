$.noConflict();

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
                $('#enter-input-name').val("");
                setTimeout(function () {
                    document.getElementById("code-input").style.display = "none";
                    document.getElementById("name-input").style.display = "block";
                    document.getElementById("name-input").style.opacity = "1";
                }, 250);

                setTimeout(function () {
                    $('#enter-input-name').focus();
                    //     $("#enter-input-name").ready(function (x) {
                    //         $('#enter-input-name').focus()
                    //     });
                    listen_on_enter(data);
                }, 1000);
            } else {
                highlight_input_code();
            }
        },
        error: function (xhr, status, error) {
            console.log("Error while editing consent date: " + error);
        },
    });
}

function listen_on_enter(data) {
    document.getElementById("arrow-name-input-enter").onclick = function () {
        let enter_input_name = $("#enter-input-name").val();
        window.location = '/agile/estimate/' + data.code + '/' + enter_input_name;
    };
}


function validate(evt) {
    let theEvent = evt || window.event;
    let key;
    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
        // Handle key press
        key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
    }
    let regex = /[0-9]|\./;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
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
            enter_input.css("color", "#f0f0f0");
        }
    });

    // $("#enter-input-code").ready(function (x) {
    //     $('#enter-input-code').focus()
    // });
    $('#enter-input-code').val("");
    setTimeout(function () {
        $('#enter-input-code').focus();
    }, 2000);

    let enter_modal = $("#enter-room-button");
    enter_modal.on("click", function () {
        // let my_css_class = {'-webkit-filter': 'blur(3px) grayscale(90%)'};
        // $(".container").css(my_css_class);
        enter_input.val("");
    })
});


