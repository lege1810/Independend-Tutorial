//npm install websocket --save

var WebSocketServer = require('websocket').server;
var http = require('http');
var clients = []
var server = http.createServer(function(request, response) {});
server.listen(1337, function() {});

wsServer = new WebSocketServer({
    httpServer: server
});

wsServer.on('request', function(request) {
    var connection = request.accept(null, request.origin);
    clients.push(connection);

    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            var message = JSON.stringify(message.utf8Data);
            if (message.substring(1, 5) == 'sys ') {
                console.log("Sys: " + message);
                if (message.substring(1, 14) == 'sys username:') {
                    var mail = message.substring(14, message.length - 1);
                    sendCourses(mail, connection);
                }
            } else {
                console.log("Chat: " + message.utf8Data + "\n")
                for (var i = 0; i < clients.length; i++) {
                    clients[i].send(message);
                }
            }
        }
    });

    connection.on('close', function(connection) {
        //close
    });
});


var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
var dbo;

MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    dbo = db.db("myTestBase");
});

function sendCourses(mail, connection) {
    var retCourses = [];

    dbo.collection("studCorp").findOne({ 'id': 'allCourses' }, function(err, resultCourses) {
        if (err) throw err;
        allCourses = resultCourses.courses;

        dbo.collection("studCorp").findOne({ 'id': 'allUsers' }, function(err, resultUser) {
            if (err) throw err;
            var users = resultUser.users;
            var user = {};

            for (var i = 0; i < users.length; i++) {
                if (users[i].mail == mail) {
                    user = users[i];
                }
            }

            for (var j = 0; j < allCourses.length; j++) {
                for (var x = 0; x < user.ownCourses.length; x++) {
                    if (String(allCourses[j].id) == String(user.ownCourses[x])) {
                        retCourses.push(allCourses[j].name);
                    }
                }
            }

            connection.send("sys coureses:" + JSON.stringify(retCourses));
        });
    });
}