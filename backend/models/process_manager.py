class ProcessManager:
    process_list = []
    
    # def __init__(self):
    #     pass

    @classmethod
    def add(cls, id: str, strat_id: str, process):
        cls.process_list.append({
            'id': id,
            'strat_id': strat_id,
            'process': process
        })

    @classmethod
    def remove(cls, id: str = None, strat_id: str = None, process = None):
        if id is not None:
            remove_list = [x for x in cls.process_list if x['id'] == id]
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