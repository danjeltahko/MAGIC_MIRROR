from flask import Flask, render_template

from moa import MOA


app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('user_menu.html')

@app.route('/m-m')
def magic_mirror():
    trains = MOA.get_trains()
    return render_template('index.html', trains=trains)

@app.route('/hue-lights')
def adjust_lights():
    return render_template('lights.html')

@app.route('/traffic')
def adjust_traffic():
    trains = MOA.get_trains()
    return render_template('traffic.html', trains=trains)

if __name__ == "__main__":
    MOA = MOA()
    app.debug = True
    app.run(host='0.0.0.0', port='1312')
