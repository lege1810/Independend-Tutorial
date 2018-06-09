window.addEventListener("load", function() {
    window.WebSocket = window.WebSocket || window.MozWebSocket;

    var connection = new WebSocket('ws://localhost:1337');

    connection.onopen = function() {
        console.log('Connected');
        connection.send("sys username:" + document.getElementById("mail").value);
    };

    connection.onerror = function(error) {
        console.log('Error');
    };

    connection.onmessage = function(message) {
        try {
            if (message.data.substring(0, 4) == 'sys ') {
                if (message.data.substring(0, 13) == 'sys coureses:') {
                    var courses = JSON.parse(message.data.substring(13, message.data.lengh));
                    var listBox = document.getElementById('tutorium');

                    courses.forEach(element => {
                        var values = element.split("_");
                        var opt = document.createElement("option");
                        listBox.options.add(opt);
                        opt.text = values[0];
                        opt.value = values[1];
                    });

                    changeTutorium(connection);
                } else if (message.data.substring(0, 12) == 'sys oldChat:') {
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

    addListeners();
});


// ###################### draggable chat ######################

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


// ###################### helper functions ######################

function addContent(nickname, message) {
    var content = document.getElementById("content");
    if (content.innerHTML != '') {
        content.innerHTML = "<br>" + content.innerHTML;
    }
    content.innerHTML = '<b>' + nickname + '</b>: ' + message + content.innerHTML;
}

function changeTutorium(connection) {
    connection.send('sys selectedTut:' + getTutorium());
    document.getElementById("content").innerHTML = '';
}

function getTutorium() {
    var tutorium = document.getElementById("tutorium");
    if (tutorium.selectedIndex != -1) {
        return tutorium.options[tutorium.selectedIndex].value;
    } else {
        return '';
    }
}