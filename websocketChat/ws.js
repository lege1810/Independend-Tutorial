//npm install websocket --save

var WebSocketServer = require('websocket').server;
var http = require('http');
var clients = []
var server = http.createServer(function(request, response) {
    // process HTTP request. Since we're writing just WebSockets
    // server we don't have to implement anything.
});
server.listen(1337, function() {});

// create the server
wsServer = new WebSocketServer({
    httpServer: server
});

// WebSocket server
wsServer.on('request', function(request) {
    var connection = request.accept(null, request.origin);
    clients.push(connection)
        // This is the most important callback for us, we'll handle
        // all messages from users here.
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            // process WebSocket message
            console.log("Nachricht : " + JSON.stringify(message.utf8Data))
            for (var i = 0; i < clients.length; i++) {
                clients[i].send(JSON.stringify(message.utf8Data))
            }
        }
    });

    connection.on('close', function(connection) {

    });
});


var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    var dbo = db.db("myTestBase");

    dbo.collection("studCorp").findOne({ 'id': 'allCourses' }, function(err, resultCourses) {
        if (err) throw err;
        allCourses = resultCourses.courses;

        dbo.collection("studCorp").findOne({ 'id': 'allUsers' }, function(err, resultUser) {
            if (err) throw err;
            var users = resultUser.users;
            var user = {};

            for (var i = 0; i < users.length; i++) {
                if (users[i].mail == 'm.maart@gmx.net') {
                    user = users[i];
                }
            }

            for (var j = 0; j < allCourses.length; j++) {
                for (var x = 0; x < user.ownCourses.length; x++) {
                    if (String(allCourses[j].id) == String(user.ownCourses[x])) {
                        console.log("-->" + allCourses[j].name);
                    }
                }
            }
            db.close();
        });
        db.close();
    });
});