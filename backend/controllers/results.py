# -*- coding: utf-8 -*-

from flask import Blueprint, request
from models.result import Result
from services.results import get_result, get_all_results, delete_result, delete_all_results
import json

results_controller = Blueprint('results_controller', __name__)

@results_controller.route('/api/results/', defaults={'id': None, 'label': None})
@results_controller.route('/api/results/id/<id>/', defaults={'label': None})
@results_controller.route('/api/results/label/<label>/', defaults={'id': None})
def results(id, label):
    if id is not None:
        result = get_result(id)
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