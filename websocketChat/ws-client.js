window.addEventListener("load", function() {
    // if user is running mozilla then use it's built-in WebSocket
    window.WebSocket = window.WebSocket || window.MozWebSocket;

    var connection = new WebSocket('ws://192.168.178.112:1337');

    connection.onopen = function() {
        console.log('Connected');
        connection.send("sysnachticht-user:" + document.getElementById("name").value);
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

    addListeners();
});

function getTutorium() {
    var tutorium = document.getElementById("tutorium");
    return tutorium.options[tutorium.selectedIndex].value;
}

function addListeners() {
    document.getElementById('dragContainer').addEventListener('mousedown', mouseDown, false);
    window.addEventListener('mouseup', mouseUp, false);

}

function mouseUp() {
    window.removeEventListener('mousemove', divMove, true);
}

function mouseDown(e) {
    window.addEventListener('mousemove', divMove, true);
}

function divMove(e) {
    var div = document.getElementById('contentContainer');
    div.style.position = 'absolute';
    div.style.top = e.clientY + 'px';
    div.style.left = e.clientX + 'px';
}