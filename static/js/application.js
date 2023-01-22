
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
        document.querySelector('.container__sl').innerHTML =
        `
        <h5 class="sl__header">${SL[0].origin_name} → ${SL[0].destin_name} </h5>
        <div class="sl__break"></div>
            ${SL.map(trip =>`
            <div class="sl__time__container">
                <p class="sl__time">${trip.origin_time.substring(9, 14)} ‣ ${trip.destin_time.substring(9, 14)}</p>
                <p class="sl__time">${trip.total_time}</p>
            </div>
            <div class="sl__transport__container">
                ${trip.transports.map(transport =>`
                <p class="sl__icon ${transport.color}">${transport.line}</p>
                `).join('')}
            </div>
            <div class="sl__break"></div>
            `).join('')}`;
    });

    socket.on('todo', function(to_do) {
        document.querySelector('.container__todo').innerHTML = 
        `<h4 class="todo__list__name">${to_do.name}</h4>
        <div class="sl__break"></div>
        <ul class="todo__list">
            ${to_do.tasks.map(task => `
            <li class="todo_list_task">${task}</li>`).join('')}
        </ul>
        <div class="sl__break"></div>`;
    });

    socket.on('fitbit', function(fitbit) {
        document.querySelector('.container__fitbit').innerHTML = 
        `<h4 class="fitbit__summary">${fitbit['summary']}</h4>
        <div class="sl__break"></div>
            ${fitbit.data.map(sleep =>
            `<div class="fitbit__total_sleep__container">
                <div class="fitbit__total_sleep_date">
                    <p class="fitbit__total_sleep_day">${sleep['day']}</p>
                    <p class="fitbit__total_sleep_time">${sleep.start.substring(11, 16)}‣${sleep.end.substring(11, 16)}</p>
                </div>
                <p class="fitbit__total_sleep_summary">${sleep['hours']}h ${sleep['minutes']}min</p>
            </div>
            <div class="fitbit__sleep_bar__container">
                <div class="fitbit__sleep_bar">
                    <div class="fitbit__sleep_bar_light" style="width: ${(sleep.light/sleep.total_minutes)*100}%;">light</div>
                    <div class="fitbit__sleep_bar_deep" style="width: ${(sleep.deep/sleep.total_minutes)*100}%;">deep</div>
                    <div class="fitbit__sleep_bar_rem" style="width: ${(sleep.rem/sleep.total_minutes)*100}%;">rem</div>
                </div>
            </div>
            `).join('')}
        `;
    });

    socket.on('weather_current', function(weather_current) {
        document.querySelector('.container__weather__current').innerHTML =
        `<div class="container__weather__current_top">
            <div class="container__weather__icon">
                <img class="weather__current__icon" src="${weather_current.icon}" alt="weather_icon">
            </div>
            <h1 class="weather__current__temperature">${weather_current.temperature}</h1>
        </div>
        <div class="sl__break"></div>
        <div class="container__weather__current_bot">
            <h5 class="weather__description">${weather_current.description}</h5>
            <p class="weather__feels_like">Känns som ${weather_current.feels_like}</p>
            <div class="sub__weather_description">
                <p class="sub__weather_description_text">M : ${weather_current.clouds}</p>
                <div class="row_break"></div>
                <p class="sub__weather_description_text">V : ${weather_current.wind}</p>
            </div>
        </div>`;
    })

    socket.on('weather_forecast', function(weather_forecast) {
        document.querySelector('.container__weather__forecast').innerHTML =
        `<div class="container__weather__forecast_hours">
            <div class="row_break_forecast"></div>
            ${weather_forecast.map(forecast => `
            <div class="weather__forecast_hour">
                <img class="weather__forecast__icon" src="${forecast.icon}" alt="weather_icon">
                <p class="weather__forecast__temperature">${forecast.temperature}</p>
                <p class="weather__forecast__time">${forecast.dt.substring(9, 14)}</p>
            </div>
            <div class="row_break_forecast"></div>`).join('')}
        </div>`;
    })
    
});