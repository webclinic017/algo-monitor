from models.base_class import BaseClass

class Strat(BaseClass):
    def __init__(self, id: str, params: dict, entry_path: str):
        self.id = id
        self.params = params
        self.entry_path = entry_path