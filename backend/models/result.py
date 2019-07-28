from models.base_class import BaseClass

class Result(BaseClass):
    def __init__(self, id: str, config: dict, result: dict = None):
        self.id = id
        self.config = config
        self.result = result