# -*- coding: utf-8 -*-

from flask import Blueprint, request
import json
from models.process_manager import ProcessManager
from models.strat import Strat
from services.strats_service import post_strat, get_strat_obj, run_strat, save_strat, create_config, get_strats_list, save_post_strat, delete_strat
from werkzeug import secure_filename
import uuid
from threading import Thread

strat_controller = Blueprint('strat_controller', __name__)

ALLOWED_EXTENSIONS = ['zip']

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
    strat_id = str(uuid.uuid4())
    name = request.form['strat_name']
    description = request.form['strat_description']
    entry_path = request.form['entry_path']
    params = json.loads(request.form['params'])
    
    strat = Strat(strat_id,name,description,params,entry_path)

    thread = Thread(target=save_post_strat,args=(file.read(), strat))
    thread.setName(f'{strat.name} : {strat.id}')
    ProcessManager.uploading_add(thread)
    thread.start()

    # success = save_strat(file.read(), strat)
    # if not success: 
    #     return json.dumps({'status': 'error', 'code': 4}), 400, {'ContentType':'application/json'}
    # post_strat(strat)

    return json.dumps({'status': 'success', 'strat_id': strat_id}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/get-upload-queue/')
def get_upload_queue():
    process_list = ProcessManager.uploading_get_all()
    return json.dumps(process_list), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/remove-upload-queue/', methods=['POST'])
def remove_upload_queue():
    json_r = request.get_json()
    strat_process_id = json_r['strat_process_id']
    removed = ProcessManager.uploading_remove(strat_process_id)

    if len(removed) == 0: return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}

    return json.dumps({'status': 'success', 'removed': removed}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/get-download-queue/')
def get_download_queue():
    process_list = ProcessManager.downloading_get_all()
    return json.dumps(process_list), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/remove-download-queue/', methods=['POST'])
def remove_download_queue():
    json_r = request.get_json()
    strat_process_id = json_r['strat_process_id']
    removed = ProcessManager.downloading_remove(strat_process_id)

    if len(removed) == 0: return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}

    return json.dumps({'status': 'success', 'removed': removed}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/run/', methods=['POST'])
def run():
    json_r = request.get_json()
    strat_id = json_r['strat_id']
    label = json_r['label']
    params = json_r['params']

    run_id = str(uuid.uuid4())
    strat = get_strat_obj(strat_id)

    if strat is None:
        return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}

    strat_data = {
        'run_id': run_id,
        'strat_id': strat_id,
        'strat': strat.name,
        'label': label
    }

    config = []
    for p in params:
        config.append({**strat_data, **p})

    create_config(run_id, strat, config)
    ProcessManager.add(run_id, strat_id)

    return json.dumps({'status': 'success', 'run_id': run_id, 'strat_id': strat_id}), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/queue/')
def get_queue():
    return ProcessManager.get_json_queue(), 200, {'ContentType':'application/json'}

@strat_controller.route('/api/strat/delete/', methods=['POST'])
def strat_delete():
    json_r = request.get_json()
    strat_id = json_r['strat_id']
    success = delete_strat(strat_id)

    if not success: return json.dumps({'status': 'error', 'code': 1}), 200, {'ContentType':'application/json'}

    return json.dumps({'status': 'success', 'strat_id': strat_id}), 200, {'ContentType':'application/json'}