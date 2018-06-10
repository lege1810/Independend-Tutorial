window.addEventListener("load", function() {
    window.WebSocket = window.WebSocket || window.MozWebSocket;

    var connection = new WebSocket('ws://localhost:1337');

    connection.onopen = function() {
        connection.send('sys selectedTut:' + getTutorium());
    };

    connection.onerror = function(error) {
        console.log('Error');
    };

    connection.onmessage = function(message) {
        try {
            if (message.data.substring(0, 4) == 'sys ') {
                if (message.data.substring(0, 12) == 'sys oldChat:') {
                    var content = document.getElementById("content");
                    var messages = JSON.parse(message.data.substring(12, message.data.lengh));
                    messages.forEach(msg => {
                        addContent(msg['nickname'], msg['message']);
                    });
                }
            } else {
                var json = JSON.parse(JSON.parse(message.data));
                if (getTutorium() == json.tutorium) {
                    addContent(json['name'], json['message']);
                }
            }
        } catch (e) {
            console.log('This doesn\'t look like a valid JSON: ',
                message.data);
            return;
        }
    };

    //change tutorium event
    document.getElementById("tutorium").addEventListener("change", function() {
        changeTutorium(connection);
    });

    //click "send" event
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


// ###################### helper functions ######################

function addContent(nickname, message) {
    var content = document.getElementById("content");
    if (content.innerHTML.trim() != "") {
        content.innerHTML = '<br>' + content.innerHTML;
    }
    content.innerHTML = '<b>' + nickname + '</b>: ' + message + content.innerHTML;
}

function changeTutorium(connection) {
    connection.send('sys selectedTut:' + getTutorium());
    document.getElementById("content").innerHTML = '';
}

function getTutorium() {
    var tutorium = document.getElementById("tutorium");
    return tutorium.value;
}