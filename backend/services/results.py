from models.result import Result
from repository.firestore import save as fs_save, get as fs_get, get_all as fs_get_all
import os
import glob
import json
from helpers.helpers import is_json

_collection = 'results'

def save_result(result: Result):
    fs_save(_collection, result.id, result.toDict())

def get_result(id: str):
    result_dict = fs_get(_collection, id)
    if result_dict is None: return None
    return Result.fromDict(result_dict)

def get_all_results(label: str = None):
    results = Result.fromListDict(fs_get_all(_collection))
    if label is not None:
        results = [r for r in results if r.label == label]
    return results

def read_local_results(id = None, strat_id = None, label = None):
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
    
    if id is not None:
        results_flatten = [r for r in results_flatten if r['id'] == id]

    if label is not None:
        results_flatten = [r for r in results_flatten if r['label'] == label]
        
    results_list = Result.fromListDict(results_flatten)
    
    return results_list

def delete_local_results(id = None, strat_id = None, label = None):
    files_to_remove = []
    if strat_id is not None:
        files_to_remove = list(set(glob.glob(f'public/strat_{strat_id}/result_*.json')))
        for f in files_to_remove[:]:
            with open(f, 'r') as file:
                txt = file.read()
                if not is_json(txt):
                    files_to_remove.remove(f)

    elif id is not None or label is not None:
        files_to_remove = list(set(glob.glob(f'public/**/result_*.json')))
        for f in files_to_remove[:]:
            with open(f, 'r') as file:
                txt = file.read()

                if not is_json(txt):
                    files_to_remove.remove(f)
                    continue

                result = Result.fromJson(txt)
                if (label is not None and result.label != label) or (id is not None and result.id != id):
                    files_to_remove.remove(f)
                    
    for f in files_to_remove:
        os.remove(f)

    return files_to_remove

def dump_local_results(strat_id):
    results = read_local_results(strat_id=strat_id)
    for r in results: save_result(r)
    delete_local_results(strat_id=strat_id)