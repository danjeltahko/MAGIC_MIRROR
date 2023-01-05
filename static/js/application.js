$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect();
    var numbers_received = [];

    //receive details from server
    socket.on('time', function(time) {
        document.getElementsByTagName('li')[0].innerHTML = time;
    });

});