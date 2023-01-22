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
    return render_template('user_menu.html', MOA=MoA)

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
            return render_template('traffic.html', trains=MoA.get_travel())

        # If 'from' is same but 'to' is different: new id search for 'to'
        elif (train_from == MoA.last_from_station and train_tooo != MoA.last_tooo_station):
            MoA.set_new_tooo_station(train_tooo)

        # If 'from' is different but 'to' is same: new id search for 'from'
        elif (train_from != MoA.last_from_station and train_tooo == MoA.last_tooo_station):
            MoA.set_new_from_station(train_from)

        # If both searches are different: new id search for both stations
        else:
            MoA.set_new_from_station(train_from)
            MoA.set_new_tooo_station(train_tooo)
        
        # Sets new travel 
        MoA.log_data(f"APP /traffic/ : new destination request is set from user")
        MoA.set_new_travel()

    return render_template('traffic.html', trains=MoA.get_travel())

@app.route("/todo-list/", methods=['POST', 'GET'])
def todo_list():
    """ 
        if todo is activated, render user_todo template
        if not, redirect to /login/todo/
    """
    if (MoA.todo_active):

        if (request.method == 'POST'):
            input_task = request.form['todo__task']
            if (len(input_task) != 0):
                MoA.add_new_task(input_task)

        todo_refreshed = MoA.get_list()
        MoA.todo_refreshed_user = True
        MoA.todo_refreshed = True
        return render_template('user_todo.html', todo_list=todo_refreshed)
    
    else:
        MoA.log_data(f"APP /todo-list/ : Microsoft TODO not activated, redirected to /login/todo/")
        return redirect("/login/todo")

@app.route("/fitbit/")
def fitbit():
    """ 
    When fitbit button is pressed in /user/
    If fitbit is activated -> redirect to /user/ and button will disappear 
    If fitbit is not activated -> redirect to /login/fitbit/ for activation
    """
    if (MoA.fitbit_active):
        return redirect("/user/")
    else:
        MoA.log_data(f"APP /fitbit/ : Fitbit not activated, redirected to /login/fitbit/")
        return redirect("/login/fitbit")

@app.route("/todo-list/change-list/", methods=['POST', 'GET'])
def change_todo_list():
    """ inside user todo, change list for mirror & user interface """
    if (MoA.todo_active):

        if (request.method == 'POST'):
            
            if ('todo-list' in request.form):
                MoA.log_data(f"APP /todo-list/change-list/ : User changed Microsoft TODO list -> {'TODO'}")
                MoA.todo_list["name"] = "TODO"
                return redirect("/todo-list/")

            elif ('shopping-list' in request.form):
                MoA.log_data(f"APP /todo-list/change-list/ : User changed Microsoft TODO list -> {'Inköpslista'}")
                MoA.todo_list["name"] = "Inköpslista"
                return redirect("/todo-list/")

            elif ('purchase' in request.form):
                MoA.log_data(f"APP /todo-list/change-list/ : User changed Microsoft TODO list -> {'Handla'}")
                MoA.todo_list["name"] = "Handla"
                return redirect("/todo-list/")
            
            else:
                return render_template('user_change_todo.html')
        else:
            return render_template('user_change_todo.html')
    else:
        return redirect("/user/")

@app.route("/login/<application>/")
def test_login_auth(application):

    # If we have to authenticate Microsoft To Do 
    # redirecting to Microsoft url for authentication
    # which in turn will redirect to our /getAzureToken
    if (application == 'todo'):
        auth_url = MoA.get_todo_auth()
        MoA.log_data(f"APP /login/todo/ : Redirecting to Microsoft for Authorization")
        return redirect(auth_url)

    # If we have to log in and authenticate Fitbit
    # redirecting to fotbit url for authentication
    # which in turn will redirect to our /getFitbitToken
    elif (application == 'fitbit'):
        auth_url = MoA.get_fitbit_auth()
        MoA.log_data(f"APP /login/fitbit/ : Redirecting to Fitbit for Authorization")
        return redirect(auth_url)

    # If application ID doesnt match with any application
    else:
        MoA.log_data(f"[ERROR] APP /login/{application} : Tried to log in to {application}, but not found")
        return render_template('404.html', data={"page": "Log in", "variable": application})

@app.route("/getAzureToken/")
def get_todo_token():

    if (request.args.get('error')):
        MoA.log_data(f"[ERROR] APP /getAzureToken/ : Authorized Failed! Could not receive access token ")
        return redirect("/user/")
    else:
        code_token = request.args.get('code')
        MoA.log_data(f"APP /getAzureToken/ : Authorized Successfully! Code Token from url received")
        MoA.set_todo_auth(code_token)
        MoA.todo_list["name"] = "Inköpslista"
        return redirect("/todo-list/")

@app.route("/getFitbitToken/")
def get_fitbit_token():

    if (request.args.get('error')):
        MoA.log_data(f"ERROR] APP /getFitbitToken/ : Authorized Failed! Could not receive access token")
    else:
        code_token = request.args.get('code')
        MoA.log_data(f"APP /getFitbitToken/ : Successfully Authorized! Code token from url received")
        MoA.set_fitbit_auth(code_token)
        MoA.fitbit_refreshed = True

    return redirect("/user/")

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
            # refreshes weather & fitbit data every minute
            if (MoA.minute_time != current_time.strftime("%H:%M")):
                MoA.weather_refresh = True
                MoA.todo_refreshed = True
                MoA.fitbit_refreshed = True
                MoA.minute_time = current_time.strftime("%H:%M")

        """ DATE """
        #  Gets & sets current date and updates page with new date
        current_date = MoA.get_current_day()
        if (MoA.current_day != current_date):
            MoA.log_data(f"APP DAY : New day!")
            socketio.emit('date', current_date)
            MoA.current_day = current_date

        """ SL TRAFFIC """
        # Checks if nearest departure has already past
        if (current_time > MoA.get_nearest_trip_time() or MoA.sl_new):

            # if current time is greater than next departure
            if (current_time > MoA.get_nearest_trip_time()):
                MoA.log_data(f"APP SL: refreshed destination schedule, current_time({current_time.strftime('%H:%M:%S')}) - train_time({MoA.get_nearest_trip_time().strftime('%H:%M:%S')})")
                MoA.set_new_travel()

            MoA.sl_new = False
            travel = MoA.get_travel()
            socketio.emit('sl', travel)

        """ TODO """
        if (MoA.todo_active):

            if (MoA.todo_expires <= datetime.now()):
                MoA.log_data(f"APP TODO : Access token expires soon!")
                MoA.todo_refresh_auth_token()

            if (MoA.todo_refreshed):
                # if get/post request was just made by user
                if (MoA.todo_refreshed_user):
                    todo_list = MoA.todo_list
                    MoA.todo_refreshed_user = False
                else:
                    todo_list = MoA.get_list()

                socketio.emit('todo', todo_list)
                MoA.todo_refreshed = False
                MoA.log_data(f"APP TODO : Updated Mirror with new data from Microsoft TODO")

        """ FITBIT """
        if (MoA.fitbit_active):

            if (MoA.fitbit_expires <= datetime.now()):
                MoA.log_data(f"APP FITBIT : Access token expires soon!")
                MoA.fitbit_refresh_auth_token()

            if (MoA.fitbit_refreshed):
                fitbit_sleep = MoA.set_sleep_summary()
                socketio.emit('fitbit', fitbit_sleep)
                MoA.fitbit_refreshed = False
                MoA.log_data(f"APP FITBIT : Updated Magic Mirror with new data from fitbit")

        """ WEATHER """
        if (MoA.weather_refresh):
            new_current_weather = MoA.set_current_weather()
            print("New weather set")
            MoA.weather_refresh = False
        


if __name__ == '__main__':
    MoA = MOA()
    socketio.run(app, host='0.0.0.0', port=1312)