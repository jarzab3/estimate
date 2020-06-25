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

function web_socket() {
//     let exampleSocket = new WebSocket("wss://localhost:8000", "protocolOne");
//     exampleSocket.send("Here's some text that the server is urgently awaiting!");
    let lo = new WebSocket("ws://localhost:8000/ws/live-score/1");
    lo.onmessage = (data) => console.log(data);
    lo.onopen = () => {
        console.log("sending city");
        lo.send(JSON.stringify({"game_city": 1}));
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

    let try_button = $('#try-it');
    try_button.click(function () {
        web_socket();
        console.log("asd");
    });

});



