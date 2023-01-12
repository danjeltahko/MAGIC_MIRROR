
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

    // receive SL from MOA
    socket.on('sl', function(SL) {
        var sl_travel = SL;
        document.querySelector('.sl').innerHTML = 
      `<h3>${sl_travel[0].origin_name} -> ${sl_travel[0].destin_name}</h3>
       ${sl_travel.map(trip => `<p>${trip.origin_time.substring(9, 14)} -> ${trip.destin_time.substring(9, 14)}</p>`).join('')}`;
    });

    socket.on('todo', function(to_do) {
        document.querySelector('.todo').innerHTML = 
        `<h3>${to_do.name}</h3>
        ${to_do.tasks.map(task => `<p>${task}</p>`).join('')}`;

    });

});