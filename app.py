try:
    from flask import Flask, render_template, request
    from flask_socketio import SocketIO
    from threading import Thread, Event
    from datetime import datetime
    from moa import MOA

except ImportError as e:
    print(e)


__author__ = 'https://github.com/DanjelTahko'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()

# View Decoration
@app.route("/")
def index():
    return render_template("main.html", clock=MoA)

@app.route("/user/")
def user_navigation():
    return render_template('user_menu.html')

@app.route('/testing')
def weather_test():
    current_weather = MOA.get_weather()
    forecast = MOA.get_forecast_today()
    return render_template('weather.html', current_weather=current_weather, today=forecast)

@app.route('/m-m')
def magic_mirror():
    trains = MOA.get_trains()
    forecast = MOA.get_forecast()
    return render_template('magic_mirror.html', trains=trains, forecast=forecast)

@app.route('/hue-lights')
def adjust_lights():
    return render_template('lights.html')

@app.route('/traffic/', methods=['POST', 'GET'])
def adjust_traffic():

    # if request.method == 'POST':
    #     changed_train_from = request.form['From']
    #     changed_train_tooo = request.form['To']
    #     MOA.search_trains(changed_train_from, changed_train_tooo)

    # trains = MOA.get_trains()
    print("in traffic")
    trains = [
        {'name': "Vällingby",
        'destination_name': "Sankt Eriksplan",
        'departure_planned': "20:15",
        'arrivaltime_planned': "20:40"},

        {'name': "Vällingby",
        'destination_name': "Sankt Eriksplan",
        'departure_planned': "20:15",
        'arrivaltime_planned': "20:40"},

        {'name': "Vällingby",
        'destination_name': "Sankt Eriksplan",
        'departure_planned': "20:15",
        'arrivaltime_planned': "20:40"},

        {'name': "Vällingby",
        'destination_name': "Sankt Eriksplan",
        'departure_planned': "20:15",
        'arrivaltime_planned': "20:40"},
    ]
    return render_template('traffic.html', trains=trains)

# Event Decoration 
@socketio.on('connect')
def send_time():
    MoA.connected += 1
    print(f"\nCONNECTED : {MoA.connected}\n")
    global thread
    if not thread.is_alive():
        print("Staring Thread")
        thread = socketio.start_background_task(moa_thread)

@socketio.on('disconnect')
def disconnect():
    MoA.connected -= 1
    print(f"\nDISCONNECTED\n")

# Thread with MOA functions
def moa_thread():
    previous_time = ''
    while not thread_stop_event.isSet():
        # Gets current time and updates page with new time
        current_time = datetime.now().strftime('%H:%M:%S')
        if (current_time != previous_time):
            socketio.emit('time', current_time)
            previous_time = current_time



if __name__ == '__main__':
    MoA = MOA()
    socketio.run(app, host='0.0.0.0', port=1312)