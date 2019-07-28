from models.result import Result
from repository.firestore import save as fs_save, get as fs_get, get_all as fs_get_all, delete as fs_delete, delete_all as fs_delete_all
import os
import glob
import json
from helpers.helpers import is_json

_collection = 'results'

def save_result(result: Result):
    fs_save(_collection, result.id, result.toDict())

def get_result(result_id: str):
    result_dict = fs_get(_collection, result_id)
    if result_dict is None: return None
    return Result.fromDict(result_dict)

def get_all_results(label: str = None):
    results = Result.fromListDict(fs_get_all(_collection))
    if label is not None:
        results = [r for r in results if r.config['label'] == label]
    return results

def delete_result(result_id: str):
    fs_delete(_collection, result_id)

def delete_all_results(label):
    fs_delete_all(_collection, lambda x, label=label: x['config']['label'] == label)

def read_local_results(run_id = None, result_id = None, strat_id = None, label = None):
    if strat_id is not None:
        files = list(set(glob.glob(f'public/strat_{strat_id}/result_*.json')))
    else:
        files = list(set(glob.glob(f'public/**/result_*.json')))

    results = []
    for f in files:
        with open(f, 'r') as file:
            txt = file.read()
            json_r = json.loads(txt)
            if is_json(txt):
                results.append(json_r)
    
    results_flatten = []
    for r in results:
        if isinstance(r, list):
            results_flatten = results_flatten + r
        else:
            results_flatten.append(r)
    
    if run_id is not None:
        results_flatten = [r for r in results_flatten if r['config']['run_id'] == run_id]

    if result_id is not None:
        results_flatten = [r for r in results_flatten if r['id'] == result_id]

    if label is not None:
        results_flatten = [r for r in results_flatten if r['config']['label'] == label]
    
    results_list = Result.fromListDict(results_flatten) # TODO: result errado trava aqui, e processo continua ativo na tela, além de travar a fila
    
    return results_list

def delete_local_results(run_id = None, result_id = None, strat_id = None, label = None):
    files_to_remove = []
    if strat_id is not None:
        files_to_remove = list(set(glob.glob(f'public/strat_{strat_id}/result_*.json')))
        for f in files_to_remove[:]:
            with open(f, 'r') as file:
                txt = file.read()
                if not is_json(txt):
                    files_to_remove.remove(f)

    elif run_id is not None or result_id is not None or label is not None:
        files_to_remove = list(set(glob.glob(f'public/**/result_*.json')))
        for f in files_to_remove[:]:
            with open(f, 'r') as file:
                txt = file.read()

                if not is_json(txt):
                    files_to_remove.remove(f)
                    continue

                result = Result.fromJson(txt)
                if (run_id is not None and result.config['run_id'] != run_id) or (result_id is not None and result.id != result_id) or (label is not None and result.config['label'] != label):
                    files_to_remove.remove(f)
                    
    for f in files_to_remove:
        os.remove(f)

    return files_to_remove

def dump_local_results(run_id):
    try:
        results = read_local_results(run_id=run_id)
        for r in results: save_result(r)
        delete_local_results(run_id=run_id)
    except TypeError:
        delete_local_results(run_id=run_id)