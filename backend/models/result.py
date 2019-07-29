# -*- coding: utf-8 -*-

from models.base_class import BaseClass

class Result(BaseClass):
    def __init__(self, id: str, config: list, result: dict = None):
        self.id = id
        self.config = config
        self.result = result