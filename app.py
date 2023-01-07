try:
    from flask import Flask, render_template, request
    from flask_socketio import SocketIO
    from threading import Thread, Event
    from datetime import datetime
    import json
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
    return render_template("main.html", MOA=MoA)

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

    if request.method == 'POST':
        changed_train_from = request.form['From']
        changed_train_tooo = request.form['To']
        print(changed_train_tooo)
        print(changed_train_tooo)
        MoA.set_new_travel(changed_train_from, changed_train_tooo)


    trains = MoA.get_travel()

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


def moa_thread():

    # Magic Mirror thread loop with MOA functions
    while not thread_stop_event.isSet():
        
        """ TIME """
        # Gets & sets current time and updates page with new time
        current_time = MoA.get_current_time()
        if (MoA.current_time != current_time):
            socketio.emit('time', current_time.strftime('%H:%M:%S'))
            MoA.current_time = current_time

        """ DATE """
        #  Gets & sets current date and updates page with new date
        current_date = MoA.get_current_day()
        if (MoA.current_day != current_date):
            socketio.emit('date', current_date)
            MoA.current_day = current_date

        """ SL TRAFFIC """
        # Checks if nearest departure has already past
        if (MoA.current_time > MoA.get_nearest_trip_time() or MoA.sl_refreshed):

            if (MoA.sl_refreshed):
                MoA.sl_refreshed = False
            else:
                print("Refreshed SL from thread")
                MoA.refresh_travel()

            socketio.emit('sl', MoA.sl_travel)






if __name__ == '__main__':
    MoA = MOA()
    socketio.run(app, host='0.0.0.0', port=1312)