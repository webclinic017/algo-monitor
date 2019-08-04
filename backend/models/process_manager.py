# -*- coding: utf-8 -*-

import datetime
import json
import copy

class ProcessManager:
    _process_list = []
    _uploading_list = []
    _downloading_list = []
    
    # def __init__(self):
    #     pass

    @classmethod
    def add(cls, run_id: str, strat_id: str, start=None, process=None):
        cls._process_list.append({
            'run_id': run_id,
            'strat_id': strat_id,
            'process': process,
            'start': start
        })
    
    @classmethod
    def get_next(cls):
        if len(cls._process_list) > 0:
            return cls._process_list[0]
        return None

    @classmethod
    def get_queue_length(cls):
        return len(cls._process_list)

    @classmethod
    def add_process(cls, run_id: str, process):
        found = [x for x in cls._process_list if x['run_id'] == run_id]
        if len(found) > 0:
            run = found[0]
            run['process'] = process
            run['start'] = datetime.datetime.utcnow()
    
    @classmethod
    def is_strat_queued(cls, strat_id: str):
        return len([x for x in cls._process_list if x['strat_id'] == strat_id]) == 0

    @classmethod
    def remove(cls, run_id: str = None, strat_id: str = None, process = None):
        if id is not None:
            remove_list = [x for x in cls._process_list if x['run_id'] == run_id]
        elif strat_id is not None:
            remove_list = [x for x in cls._process_list if x['strat_id'] == strat_id]
        elif process is not None:
            remove_list = [x for x in cls._process_list if x['process'] == process]
        else:
            return None

        if not remove_list or len(remove_list) == 0:
            return None

        cls._process_list = [x for x in cls._process_list if x not in remove_list]

        return remove_list

    @classmethod
    def get_active(cls):
        return [x for x in cls._process_list if x['process'] is not None]

    @classmethod
    def get_json_queue(cls):
        without_keys = lambda d, keys: {x: d[x] for x in d if x not in keys}
        queue = copy.deepcopy([without_keys(x, {'process'}) for x in cls._process_list])
        for q in queue:
            if q['start'] is not None:
                q['start'] = str(q['start'])
                
        return json.dumps(queue)


    @classmethod
    def uploading_add(cls, thread):
        cls._uploading_list.append(thread)

    @classmethod
    def uploading_get_all(cls):
        return [{'strat_id':x.getName(),'completed':not x.is_alive()} for x in cls._uploading_list]

    @classmethod
    def uploading_remove(cls, name):
        removed = [x.getName() for x in cls._uploading_list if (x.getName() == name and not x.is_alive())]
        cls._uploading_list = [x for x in cls._uploading_list if not (x.getName() == name and not x.is_alive())]
        return removed


    @classmethod
    def downloading_add(cls, strat_id):
        download = {
            'strat_id': strat_id,
            'completed': False
        }
        cls._downloading_list.append(download)

    @classmethod
    def downloading_update_complete(cls, strat_id):
        found = [x for x in cls._downloading_list if x['strat_id'] == strat_id]
        if len(found) > 0:
            download = found[0]
            download['completed'] = True

    @classmethod
    def downloading_get_all(cls):
        return cls._downloading_list

    @classmethod
    def downloading_remove(cls, strat_id):
        removed = [x for x in cls._downloading_list if x['strat_id'] == strat_id and x['completed'] == True]        
        cls._downloading_list = [x for x in cls._downloading_list if x['strat_id'] != strat_id]
        return removed