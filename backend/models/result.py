from models.base_class import BaseClass

class Result(BaseClass):
    def __init__(self, id: str, label: str, config: dict, result: dict = None):
        self.id = id
        self.label = label
        self.config = config
        self.result = result