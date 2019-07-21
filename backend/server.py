# -*- coding: utf-8 -*-

import repository.firebase as fb
fb.init()

from flask import Flask, render_template, send_file, Response, request, send_from_directory
from controllers.results import results_controller
from controllers.strat import strat_controller

app = Flask(__name__, static_folder='../frontend/dist')

app.url_map.strict_slashes = False

app.register_blueprint(results_controller)
app.register_blueprint(strat_controller)

@app.route('/')
def home():
    return send_from_directory('../frontend/dist', 'index.html')

@app.route('/<path:path>')
def statics(path):
    return send_from_directory('../frontend/dist', path)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)#debug=True