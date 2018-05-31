window.addEventListener("load", function () {
    // if user is running mozilla then use it's built-in WebSocket
    window.WebSocket = window.WebSocket || window.MozWebSocket;
  
    var connection = new WebSocket('ws://127.0.0.1:1337');
  
    connection.onopen = function () {
      // connection is opened and ready to use
      document.getElementById("wsConnection").textContent = "Connected"
    };
  
    connection.onerror = function (error) {
      // an error occurred when sending/receiving data
      document.getElementById("wsConnection").textContent = "Error"
    };
  
    connection.onmessage = function (message) {
      // try to decode json (I assume that each message
      // from server is json)
      try {
        var json = JSON.parse(message.data);
      } catch (e) {
        console.log('This doesn\'t look like a valid JSON: ',
            message.data);
        return;
      }
      // handle incoming message
      var wsChatContent = document.getElementById("wsChatContent")
      wsChatContent.innerHTML = wsChatContent.innerHTML + "<br>" + message.data

    };

    document.getElementById("wsSendTextButton").addEventListener("click", function(){
        var texttoSend = document.getElementById("wsText")
        connection.send(texttoSend.value)
        texttoSend.value = ""
    });
  });