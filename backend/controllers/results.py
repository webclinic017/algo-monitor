# -*- coding: utf-8 -*-

from flask import Blueprint
from models.result import Result
from models.strat import Strat
from services.results import save_result, get_result, get_all_results
from services.strats import save_strat, get_strat, run_strat
import glob
import json

results_controller = Blueprint('results_controller', __name__)

def read_results(id = None, label = None):
    if id is not None:
        results = []
        files = list(set(glob.glob(f'public/strat_{id}/result_*.json')))
        for f in files:
            with open(f, 'r') as file:
                txt = file.read()
                json_r = json.loads(txt)
                results.append(json_r)
        return results

    results = []
    
    files = list(set(glob.glob(f'public/**/result_*.json')))
    for f in files:
        with open(f, 'r') as file:
            txt = file.read()
            json_r = json.loads(txt)
            results.append(json_r)
    
    if label is not None:
        results = [r for r in results if r['label'] == label]

    return results

@results_controller.route('/api/results', defaults={'id': None, 'label': None})
@results_controller.route('/api/results/id/<id>', defaults={'label': None})
@results_controller.route('/api/results/label/<label>', defaults={'id': None})
def results(id, label):
    results = read_results(id, label)
    return json.dumps(results)
    # result = Result('teste','teste',{'teste':'teste'},{'teste':'teste'},123,123)
    # save_result(result)
    # return Result.toListJson(get_all_results())