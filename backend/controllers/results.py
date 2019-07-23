# -*- coding: utf-8 -*-

from flask import Blueprint
from models.result import Result
from models.strat import Strat
from services.results import get_result, get_all_results
from services.strats import save_strat, get_strat, run_strat
import glob
import json

results_controller = Blueprint('results_controller', __name__)

@results_controller.route('/api/results/', defaults={'id': None, 'label': None})
@results_controller.route('/api/results/id/<id>/', defaults={'label': None})
@results_controller.route('/api/results/label/<label>/', defaults={'id': None})
def results(id, label):
    if id is not None:
        results = get_result(id).toJson()
    else:
        results = Result.toListJson(get_all_results(label=label))
    return results, 200, {'ContentType':'application/json'}