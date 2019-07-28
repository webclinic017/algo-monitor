import datetime
import json
import copy

class ProcessManager:
    process_list = []
    uploading_list = []
    
    # def __init__(self):
    #     pass

    @classmethod
    def add(cls, run_id: str, strat_id: str, start=None, process=None):
        cls.process_list.append({
            'run_id': run_id,
            'strat_id': strat_id,
            'process': process,
            'start': start
        })


    @classmethod
    def add_process(cls, run_id: str, process):
        run = [x for x in cls.process_list if x['run_id'] == run_id][0]
        run['process'] = process
        run['start'] = datetime.datetime.utcnow()

    @classmethod
    def remove(cls, run_id: str = None, strat_id: str = None, process = None):
        if id is not None:
            remove_list = [x for x in cls.process_list if x['run_id'] == run_id]
        elif strat_id is not None:
            remove_list = [x for x in cls.process_list if x['strat_id'] == strat_id]
        elif process is not None:
            remove_list = [x for x in cls.process_list if x['process'] == process]
        else:
            return None

        if not remove_list or len(remove_list) == 0:
            return None

        cls.process_list = [x for x in cls.process_list if x not in remove_list]

        return remove_list

    @classmethod
    def get_active(cls):
        return [x for x in cls.process_list if x['process'] is not None]

    @classmethod
    def get_json_queue(cls):
        without_keys = lambda d, keys: {x: d[x] for x in d if x not in keys}
        queue = copy.deepcopy([without_keys(x, {'process'}) for x in cls.process_list])
        for q in queue:
            if q['start'] is not None:
                q['start'] = str(q['start'])
                
        return json.dumps(queue)

    @classmethod
    def uploading_list_add(cls, thread):
        cls.uploading_list.append(thread)

    @classmethod
    def uploading_list_get_all(cls):
        return [{'name':x.getName(),'alive':x.is_alive()} for x in cls.uploading_list]

    @classmethod
    def uploading_list_remove(cls, name):
        removed = [x.getName() for x in cls.uploading_list if (x.getName() == name and not x.is_alive())]
        cls.uploading_list = [x for x in cls.uploading_list if not (x.getName() == name and not x.is_alive())]
        return removed