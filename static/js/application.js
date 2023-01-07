
$(document).ready(function(){

    //connect to the socket server.
    var socket = io.connect();

    // receive time from MOA
    socket.on('time', function(time) {
        document.getElementsByClassName('time')[0].innerHTML = time
    });

    // receive date from MOA
    socket.on('date', function(date) {
        document.getElementsByClassName('date')[0].innerHTML = date
    });

    // receive details from MOA
    socket.on('sl', function(SL) {
        var sl_travel = SL;
        document.querySelector('.sl').innerHTML = 
      `<h3>${sl_travel[0].origin_name} -> ${sl_travel[0].destin_name}</h3>
       ${sl_travel.map(trip => `<p>${trip.origin_time} -> ${trip.destin_time}</p>`).join('')}`;
    });

});