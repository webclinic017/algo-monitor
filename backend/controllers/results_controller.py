# -*- coding: utf-8 -*-

from flask import Blueprint, request, send_file
from models.result import Result
from services.results_service import get_result, get_all_results, delete_result, delete_all_results
from helpers.helpers import zipdir_glob
import json
import zipfile
import io
import os
import time

results_controller = Blueprint('results_controller', __name__)

@results_controller.route('/api/results/', defaults={'result_id': None, 'label': None})
@results_controller.route('/api/results/id/<result_id>/', defaults={'label': None})
@results_controller.route('/api/results/label/<path:label>/', defaults={'result_id': None})
def results(result_id, label):
    if result_id is not None:
        result = get_result(result_id)
        if result is None:
            result = json.dumps(result)
        else:
            result = result.toJson()
    else:
        result = Result.toListJson(get_all_results(label=label))
    return result, 200, {'ContentType':'application/json'}

@results_controller.route('/api/results/delete/', methods={'POST'})
def result_delete():
    json_r = request.get_json()
    result_id = json_r['result_id']
    delete_result(result_id)

    return json.dumps({'status': 'success', 'result_id': result_id}), 200, {'ContentType':'application/json'}

@results_controller.route('/api/results/delete/all', methods={'POST'})
def result_delete_all():
    json_r = request.get_json()
    label = json_r['label']
    delete_all_results(label)
    return json.dumps({'status': 'success'}), 200, {'ContentType':'application/json'}

@results_controller.route('/api/results/download/id/<result_id>/', defaults={'label': None})
@results_controller.route('/api/results/download/label/<path:label>/', defaults={'result_id': None})
def result_download(result_id, label):
    if result_id is not None:
        results = [get_result(result_id)]
    else:
        results = get_all_results(label=label)

    if results is None or len(results) == 0: return json.dumps({'status': 'error', 'code': 1}), 404, {'ContentType':'application/json'}
    
    out_path = f'public/results_{time.time()}.zip'

    zipf = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
    for r in results:
        zipf.writestr(f'result_{r.id}.json', r.toJson())
    if len(results) > 1: zipf.writestr('results.json', Result.toListJson(results))
    zipf.close()

    file = io.FileIO(out_path, 'r')
    memory_file = io.BytesIO()
    memory_file.write(file.readall())
    memory_file.seek(0)
    file.close()

    os.remove(out_path)

    return send_file(memory_file, attachment_filename='results.zip', as_attachment=True)