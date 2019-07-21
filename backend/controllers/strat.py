# -*- coding: utf-8 -*-

from flask import Blueprint, request
import json
from models.strat import Strat
from services.strats import save_strat, get_strat, run_strat, upload_strat, run_status, start_status_check
from werkzeug import secure_filename
import uuid

strat_controller = Blueprint('strat_controller', __name__)

ALLOWED_EXTENSIONS = ['zip']

process_list = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

status_job = start_status_check(process_list)

@strat_controller.route('/api/upload', methods=['POST'])
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
    entry_path = request.form['entry_path']
    id = str(uuid.uuid4())

    strat = Strat(id,{},entry_path)
    upload_strat(file.read(), strat)
    save_strat(strat)
    
    return json.dumps({'status': 'success', 'id': id}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/run', methods=['POST'])
def run():
    json_r = request.get_json()

    id = json_r['id']
    process = run_strat(id)

    if process is None: return json.dumps({'status': 'error', 'code': 1}), 400, {'ContentType':'application/json'}

    process_list.append(process)
    return json.dumps({'status': 'success'}), 200, {'ContentType':'application/json'}