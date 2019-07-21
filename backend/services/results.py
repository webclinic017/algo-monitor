from models.result import Result
from repository.firestore import save as fs_save, get as fs_get, get_all as fs_get_all

_collection = 'results'

def save_result(result: Result):
    fs_save(_collection, result.id, result.toDict())

def get_result(id: str):
    result_dict = fs_get(_collection, id)
    if result_dict is None: return None
    return Result.fromDict(result_dict)

def get_all_results():
    return [Result.fromDict(r) for r in fs_get_all(_collection)]