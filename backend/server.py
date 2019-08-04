# -*- coding: utf-8 -*-

import repository.firebase as fb
fb.init()

from flask import Flask, render_template, send_file, Response, request, send_from_directory
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter
from controllers.results_controller import results_controller
from controllers.strat_controller import strat_controller

from services.strats_service import start_status_check

import psutil
import datetime
import json
import logging

app = Flask(__name__)#, static_folder='../frontend/dist')
app.url_map.strict_slashes = False

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

status_job = start_status_check(10)

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

@app.route('/api/log/')
def view_log():
    with open('status.log', 'r') as file:
        return f'<pre>{file.read()}</pre>'

@app.route('/api/monitor/')
def monitor():
    status = get_processes()
    return json.dumps(status), 200, {'ContentType':'application/json'}

# Files # e.g. /manifest.json

@app.route('/<regex(".*\..*"):path>')
def statics(path):
    return send_from_directory('../frontend/dist', path)

# Front (catch-all) # e.g. /home

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('../frontend/dist', 'index.html')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)#debug=True