try:
    from flask import Flask, render_template, request, url_for, send_from_directory, redirect
    from flask_socketio import SocketIO
    from threading import Thread, Event
    from datetime import datetime
    import json
    import os, sys
    from moa import MOA

    import requests

except ImportError as e:
    print(e)


__author__ = 'https://github.com/DanjelTahko'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

thread = Thread()

# View Decoration
@app.route("/")
def index():
    """ View for Magic Mirror """
    return render_template("main.html", MOA=MoA)

@app.route("/user/")
def user_navigation():
    """ View for User Menu """
    return render_template('user_menu.html')

@app.route('/traffic/', methods=['POST', 'GET'])
def adjust_traffic():
    """ View for Traffic, change trip for Magic Mirror"""

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

@app.route("/todo-list/", methods=['POST', 'GET'])
def todo_list():
    
    if (MoA.todo_active):

        if (request.method == 'POST'):
            input_task = request.form['todo__task']
            MoA.add_new_task(input_task)
            MoA.log_data(f"App Route /todo-list/ 'POST' : Added new task ({input_task}) to task-list")
            get_refresh = MoA.get_list()
            MoA.todo_refreshed = True

        else:
            get_refresh = MoA.get_list()

        return render_template('user_todo.html', todo_list=get_refresh)
    
    else:
        MoA.log_data(f"App Route /todo-list : Not activated, redirected to /login/todo")
        return redirect("/login/todo")


@app.route("/fitbit/")
def fitbit():

    if (MoA.fitbit_active):
        return "Activated"

    else:
        MoA.log_data(f"App Route /fitbit : Not activated, redirected to /login/fitbit")
        return redirect("/login/fitbit")

@app.route("/todo-list/change-list/", methods=['POST', 'GET'])
def change_todo_list():

    if (MoA.todo_active):

        if (request.method == 'POST'):
            
            if ('todo-list' in request.form):
                MoA.set_other_list("TODO")
                return redirect("/todo-list/")

            elif ('shopping-list' in request.form):
                MoA.set_other_list("Inköpslista")
                return redirect("/todo-list/")

            elif ('purchase' in request.form):
                MoA.set_other_list("Handla")
                return redirect("/todo-list/")
            
            else:
                return render_template('user_change_todo.html')

        else:
            return render_template('user_change_todo.html')
    
    else:
        print("Something went wrong in 'change_todo_list' not active?")
        return redirect("/login/todo")


# Log in route for API with OAuth
@app.route("/login/<application>/")
def test_login_auth(application):

    # If we have to authenticate Microsoft To Do 
    # redirecting to Microsoft url for authentication
    # which in turn will redirect to our /getAzureToken
    if (application == 'todo'):
        # Creates authentication url 
        auth_url = MoA.get_todo_auth()
        MoA.log_data(f"App Route /login/todo : Redirecting to Microsoft for Authorization")
        print("Redirecting to Microsoft for Authorization")
        return redirect(auth_url)

    # If we have to log in and authenticate Fitbit
    # redirecting to fotbit url for authentication
    # which in turn will redirect to our /getFitbitToken
    elif (application == 'fitbit'):
        auth_url = MoA.get_fitbit_auth()
        MoA.log_data(f"App Route /login/todo : Redirecting to Fitbit for Authorization")
        print("Redirecting to Fitbit for Authorization")
        return redirect(auth_url)

    # If application ID doesnt match with any application
    else:
        MoA.log_data(f"App Route /login/{application} : Tried to log in to {application}, but not found")
        return render_template('404.html', data={"page": "Log in", "variable": application})

@app.route("/getAzureToken/")
def get_token():

    if (request.args.get('error')):
        MoA.log_data(f"App Route /getAzureToken/ : Authorized Failed! Could not receive token ")
        print("Authorized Failed!!")
    else:
        code_token = request.args.get('code')
        MoA.log_data(f"App Route /getAzureToken/ : Authorized Successfully! Token received")
        print("Authorized Successfully Token received in /getAzureToken/!!")
        MoA.set_auth(code_token)
        MoA.__TODO__()

    return redirect("/todo-list/")

@app.route("/getFitbitToken/")
def get_fitbit_token():

    if (request.args.get('error')):
        MoA.log_data(f"App Route getFitbitToken/ : Authorized Failed! Could not receive token ")
        print("Authorized Failed!!")
    else:
        code_token = request.args.get('code')
        MoA.log_data(f"App Route getFitbitToken/ : Authorized Successfully! Token received")
        print("Authorized Successfully Token received in /getAzureToken/!!")
        # MoA.set_auth(code_token)
        # MoA.set_other_list("Inköpslista")

    return redirect("/fitbit/")


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


# Event Decoration 
@socketio.on('connect')
def connect():
    MoA.connected += 1
    print(f"\nNEW CONNECTION")
    print(f"\nCONNECTED : {MoA.connected}\n")
    global thread
    if not thread.is_alive():
        print("Staring Thread")
        thread = socketio.start_background_task(moa_thread)

@socketio.on('disconnect')
def disconnect():
    MoA.connected -= 1
    print(f"\nDISCONNECTION")
    print(f"CONNECTED : {MoA.connected}\n")


def moa_thread():

    # Magic Mirror thread loop with MOA functions
    while (MoA.connected):
        
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
                data = "App Thread SL: new destination is set from user or __init__"
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

        """ TODO """
        if (MoA.todo_active):
            
            if (MoA.todo_refreshed):
                print("Sends update to socket - inside TODO thread because of refresh")
                socketio.emit('todo', MoA.todo_list)
                MoA.todo_refreshed = False
                MoA.log_data(f"App Thread TODO : Updated Mirror because of todo refresh")

            elif (MoA.todo_prev_time != current_time.strftime("%H:%M")):
                print("inside TODO thread because of time passed")
                refreshed_todo = MoA.get_list()
                socketio.emit('todo', refreshed_todo)
                MoA.log_data(f"App Thread TODO : Updated Mirror because of time passed {MoA.todo_prev_time}-{current_time.strftime('%H:%M')}")
                MoA.todo_prev_time = current_time.strftime("%H:%M")

        


if __name__ == '__main__':
    MoA = MOA()
    socketio.run(app, host='0.0.0.0', port=1312)