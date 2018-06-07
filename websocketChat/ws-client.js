window.addEventListener("load", function() {
    // if user is running mozilla then use it's built-in WebSocket
    window.WebSocket = window.WebSocket || window.MozWebSocket;

    var connection = new WebSocket('ws://127.0.0.1:1337');

    connection.onopen = function() {
        console.log('Connected');
    };

    connection.onerror = function(error) {
        console.log('Error');
    };

    connection.onmessage = function(message) {
        try {
            var json = JSON.parse(JSON.parse(message.data));
            if (getTutorium() == json.tutorium) {
                var content = document.getElementById("content");
                content.innerHTML = content.innerHTML + "<br>" + json['name'] + ': ' + json['message'];
            }
        } catch (e) {
            console.log('This doesn\'t look like a valid JSON: ',
                message.data);
            return;
        }
    };

    document.getElementById("send").addEventListener("click", function() {
        var message = document.getElementById("message");
        var name = document.getElementById("name");
        message = {
            'tutorium': getTutorium(),
            'message': message.value,
            'name': name.value
        }
        connection.send(JSON.stringify(message));
        message.value = "";
    });
});

function getTutorium() {
    var tutorium = document.getElementById("tutorium");
    return tutorium.options[tutorium.selectedIndex].value;
}