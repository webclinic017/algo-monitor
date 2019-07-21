from models.base_class import BaseClass

class Result(BaseClass):
    def __init__(self, id: str, label: str, config: dict, result: dict = None, start = None, end = None):
        self.id = id
        self.label = label
        self.config = config
        self.start = start
        self.end = end
        self.result = result