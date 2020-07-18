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

function highlight_pass_input() {
    console.log("highlight pass");
    // let enter_input = $('input#enter-input-code');
    // let code = enter_input.val();
    // if (code.length === 5) {
    //     enter_input.css("color", "red");
    // }
    let enter_password_arrow = $('#arrow-pass-input-enter');
    enter_password_arrow.css("color", "#f0f0f0");
}

function check_code(request_data) {
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: "api/validate_code",
        data: request_data,
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        success: function (data, status, xhr) {
            if (data.code != null) {
                localStorage.setItem("session_code", data.code);
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

// TODO: implement cookies to store code
function validate_password(request_data) {
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: "api/pass_validate_code",
        data: request_data,
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
        },
        success: function (data, status, xhr) {
            if (data != null) {
                console.log()
                // window.location = '/agile/estimate/' + data.code + '/' + enter_input_name;

                console.log("success entered pass");
                // $('#enter-input-name').val("");
                // setTimeout(function () {
                //     document.getElementById("code-input").style.display = "none";
                //     document.getElementById("name-input").style.display = "block";
                //     document.getElementById("name-input").style.opacity = "1";
                // }, 250);
                //
                // setTimeout(function () {
                //     listen_on_enter(data);
                // }, 1000);
            } else {
                highlight_pass_input();
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
        let is_admin = $("#chk").is(":checked");
        if (is_admin === true) {
            // go to pass view
            document.getElementById("name-input").style.opacity = "0";
            setTimeout(() => {
                document.getElementById("name-input").style.display = "none";
                document.getElementById("pass-input").style.display = "block";
            }, 500);

            // document.getElementById("arrow-pass-input-enter").onclick = function () {
            //     console.log("checking pass");
            // }

        } else {
            window.location = '/agile/estimate/' + data.code + '/' + enter_input_name;
        }
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

    let enter_password_arrow = $('#arrow-pass-input-enter');
    enter_password_arrow.on("click", function () {
        let frm = document.getElementById('enter-session-pass-form') || null;
        let enter_input_name = $('#enter-input-name').val();
        let code_from_storage = localStorage.getItem("session_code");
        // console.log(enter_input_name);
        // console.log(code_from_storage);
        if (frm) {
            frm.action = '/agile/estimate/' + code_from_storage + '/' + enter_input_name;
            frm.submit(function () {
                var csrftoken = getCookie('csrftoken');
            });
        }
    });

    let pass_input = $("#enter-input-password");
    // Execute a function when the user releases a key on the keyboard
    pass_input.on("keyup", function (event) {
        if (event.keyCode === 13) {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            enter_password_arrow.click();
            // submit_form();
        }
    });

    // $('#submitButton').click(function (event) {
    //     event.preventDefault(); //so that we stop normal form submit.
    //     let pass = $('input#enter-input-password').val();
    //     Get code from storage
    // let code_from_storage = localStorage.getItem("session_code");
    // let username = $('#enter-input-name').val();
    // let request_data = JSON.stringify({password: pass, code: code_from_storage, username: username});
    // validate_password(request_data);
    // });


    // $("#enter-input-code").ready(function (x) {
    //     $('#enter-input-code').focus()
    // });


    $('#chk').prop('checked', false);

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


