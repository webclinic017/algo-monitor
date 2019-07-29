# -*- coding: utf-8 -*-

from models.base_class import BaseClass

class Strat(BaseClass):
    def __init__(self, id: str, name: str, params: dict, entry_path: str):
        self.id = id
        self.name = name
        self.params = params
        self.entry_path = entry_path