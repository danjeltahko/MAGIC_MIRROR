try:
    from flask import Flask, render_template, request, url_for, send_from_directory
    from flask_socketio import SocketIO
    from threading import Thread, Event
    from datetime import datetime
    import json
    import os, sys
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

        # Cleans string from form so only letters will be in search
        train_from = request.form['From']
        train_from = "".join([char for char in train_from if char.isalpha()])
        train_tooo = request.form['To']
        train_tooo = "".join([char for char in train_tooo if char.isalpha()])

        # If user input from form is empty, use previous search
        if (len(train_from) == 0):
            train_from = MoA.last_from_station
        if (len(train_tooo) == 0):
            train_tooo = MoA.last_tooo_station

        # If new search is same as before: return html page with existing travel
        if (train_from == MoA.last_from_station and train_tooo == MoA.last_tooo_station):
            MoA.log_data("App Route /traffic 'POST' request: same stations as before, refresh travel")
            return render_template('traffic.html', trains=MoA.get_travel())

        # If 'from' is same but 'to' is different: new id search for 'to'
        elif (train_from == MoA.last_from_station and train_tooo != MoA.last_tooo_station):
            MoA.log_data(f"App Route /traffic 'POST' request: new to_station={train_tooo}")
            MoA.set_new_tooo_station(train_tooo)

        # If 'from' is different but 'to' is same: new id search for 'from'
        elif (train_from != MoA.last_from_station and train_tooo == MoA.last_tooo_station):
            MoA.log_data(f"App Route /traffic 'POST' request: new from_station={train_from}")
            MoA.set_new_from_station(train_from)

        # If both searches are different: new id search for both stations
        else:
            MoA.log_data(f"App Route /traffic 'POST' request: new travel search=({train_from}-{train_tooo})")
            MoA.set_new_from_station(train_from)
            MoA.set_new_tooo_station(train_tooo)
        
        # Sets new travel 
        MoA.set_new_travel()

    return render_template('traffic.html', trains=MoA.get_travel())

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
        if (MoA.current_time != current_time.strftime("%H:%M:%S")):
            socketio.emit('time', current_time.strftime('%H:%M:%S'))
            MoA.current_time = current_time.strftime("%H:%M:%S")

        """ DATE """
        #  Gets & sets current date and updates page with new date
        current_date = MoA.get_current_day()
        if (MoA.current_day != current_date):
            socketio.emit('date', current_date)
            MoA.current_day = current_date

        """ SL TRAFFIC """
        # Checks if nearest departure has already past
        if (current_time > MoA.get_nearest_trip_time() or MoA.sl_new):
            
            # if new travel destination is set by user
            if (MoA.sl_new):
                data = "App Thread SL: new destination is set from user"
                MoA.sl_new = False
                # Log data
                MoA.log_data(data)

            # if current time is greater than next departure
            elif (current_time > MoA.get_nearest_trip_time()):
                # Log data
                MoA.log_data(f"App Thread SL: refreshed destination schedule, current_time({current_time.strftime('%H:%M:%S')}) - train_time({MoA.get_nearest_trip_time().strftime('%H:%M:%S')})")
                MoA.set_new_travel()
                MoA.sl_new = False
                MoA.log_data(f"App Thread SL: new time of nearest train departure={MoA.get_nearest_trip_time().strftime('%H:%M:%S')}")
                print("Time passed")
            # if somethings wrong??
            else:
                print("App Thread SL = something is wrong..")

            travel = MoA.get_travel()
            socketio.emit('sl', travel)


if __name__ == '__main__':
    MoA = MOA()
    socketio.run(app, host='0.0.0.0', port=1312)