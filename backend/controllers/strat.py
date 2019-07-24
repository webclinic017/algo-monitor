# -*- coding: utf-8 -*-

from flask import Blueprint, request
import json
from models.process_manager import ProcessManager
from models.strat import Strat
from services.strats import save_strat, get_strat, run_strat, upload_strat, start_status_check, create_config, get_strats_list
from werkzeug import secure_filename
import uuid

strat_controller = Blueprint('strat_controller', __name__)

ALLOWED_EXTENSIONS = ['zip']

status_job = start_status_check(10)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@strat_controller.route('/api/strat/list/')
def get_list():
    strats = get_strats_list()
    return Strat.toListJson(strats), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/upload/', methods=['POST'])
def upload():
    if 'file' not in request.files:
        # flash('No file part')
        return json.dumps({'status': 'error', 'code': 1}), 400, {'ContentType':'application/json'}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        # flash('No selected file')
        return json.dumps({'status': 'error', 'code': 2}), 400, {'ContentType':'application/json'}
    if not file or not allowed_file(file.filename):
        return json.dumps({'status': 'error', 'code': 3}), 400, {'ContentType':'application/json'}
        
    filename = secure_filename(file.filename)
    id = str(uuid.uuid4())
    name = request.form['strat_name']
    entry_path = request.form['entry_path']
    params = json.loads(request.form['params'])
    
    strat = Strat(id,name,params,entry_path)
    success = upload_strat(file.read(), strat)

    if not success: 
        return json.dumps({'status': 'error', 'code': 4}), 400, {'ContentType':'application/json'}

    save_strat(strat)    
    return json.dumps({'status': 'success', 'id': id}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/run/', methods=['POST'])
def run():
    # TODO: receber params
    json_r = request.get_json()
    strat_id = json_r['strat_id']
    params = json_r['params']

    run_id = str(uuid.uuid4())
    strat = get_strat(strat_id)
    strat_data = {
        'run_id': run_id,
        'strat_id': strat_id,
        'strat': strat.name,
    }

    config = []
    for p in params:
        config.append({**strat_data, **p})

    create_config(run_id, strat_id, config)
    process = run_strat(run_id, strat_id)

    if process is None: return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}

    ProcessManager.add(run_id, strat_id, process)

    return json.dumps({'status': 'success', 'run_id': run_id, 'strat_id': strat_id}), 200, {'ContentType':'application/json'}