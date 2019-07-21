# -*- coding: utf-8 -*-

from flask import Blueprint, request
import json
from models.process_manager import ProcessManager
from models.strat import Strat
from services.strats import save_strat, get_strat, run_strat, upload_strat, start_status_check, create_config
from werkzeug import secure_filename
import uuid

strat_controller = Blueprint('strat_controller', __name__)

ALLOWED_EXTENSIONS = ['zip']

status_job = start_status_check(10)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@strat_controller.route('/api/upload/', methods=['POST'])
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
    name = request.form['name']
    entry_path = request.form['entry_path']

    strat = Strat(id,name,{},entry_path)
    upload_strat(file.read(), strat)
    save_strat(strat)
    
    return json.dumps({'status': 'success', 'id': id}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/run/', methods=['POST'])
def run():
    # TODO: receber params
    json_r = request.get_json()

    id = str(uuid.uuid4())
    strat_id = json_r['id']
    strat = get_strat(strat_id)
    create_config(id, strat_id, [{
        'id': id,
        'strat': strat.name,
        'strat_id': strat.id
    }])
    process = run_strat(id, strat_id)

    if process is None: return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}

    ProcessManager.add(id, strat_id, process)

    return json.dumps({'status': 'success', 'id': id, 'strat_id': strat_id}), 200, {'ContentType':'application/json'}