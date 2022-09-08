from crypt import methods
from urllib import request
from flask import Flask, render_template, request

from moa import MOA


app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('user_menu.html')

@app.route('/m-m')
def magic_mirror():
    trains = MOA.get_trains()
    forecast = MOA.get_forecast()
    return render_template('magic_mirror.html', trains=trains, forecast=forecast)

@app.route('/hue-lights')
def adjust_lights():
    return render_template('lights.html')

@app.route('/traffic', methods=['POST', 'GET'])
def adjust_traffic():

    if request.method == 'POST':
        changed_train_from = request.form['From']
        changed_train_tooo = request.form['To']
        MOA.search_trains(changed_train_from, changed_train_tooo)

    trains = MOA.get_trains()
    return render_template('traffic.html', trains=trains)

if __name__ == "__main__":
    MOA = MOA()
    app.debug = True
    app.run(host='0.0.0.0', port='1312')
