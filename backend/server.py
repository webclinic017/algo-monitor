# -*- coding: utf-8 -*-

import repository.firebase as fb
fb.init()

from flask import Flask, render_template, send_file, Response, request, send_from_directory
from controllers.results import results_controller
from controllers.strat import strat_controller

import psutil
import datetime
import json

app = Flask(__name__, static_folder='../frontend/dist')

app.url_map.strict_slashes = False

app.register_blueprint(results_controller)
app.register_blueprint(strat_controller)

def get_processes(search=None):
    status = []
    pids = psutil.pids()
    for pid in pids:
        process = psutil.Process(pid)
        status.append(
            {
                'name': process.name(),
                'created_date': datetime.datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    status = sorted(status, key=lambda k: k['created_date'], reverse=True)
    return status

@app.route('/')
def home():
    return send_from_directory('../frontend/dist', 'index.html')

@app.route('/log/')
def log():
    with open('status.log', 'r') as file:
        return f'<pre>{file.read()}</pre>'

@app.route('/monitor/')
def monitor():
    status = get_processes()
    return json.dumps(status), 200, {'ContentType':'application/json'} 

# @app.route('/<path:path>')
# def statics(path):
#     return send_from_directory('../frontend/dist', path)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)#debug=True