# -*- coding: utf-8 -*-

import json
import jsonpickle
import numpy as np

def convert_nan(obj):
    isnan = lambda x: isinstance(x, float) and np.isnan(x)
    if isinstance(obj, list):
        for i,e in enumerate(obj):
            if isnan(e):
              obj[i] = None
            else:
              convert_nan(e)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if isnan(v):
                obj[k] = None
            else:
                convert_nan(v)
    elif isnan(obj):
        obj = None

class nanInfPickler(jsonpickle.pickler.Pickler):
    """
    encodes float values like inf / nan as strings to follow JSON spec while keeping meaning
    Im doing this in custom class because handlers do not fire for floats
    """
    inf = float('inf')
    negativeInf = float('-inf')

    def _get_flattener(self, obj):
        if type(obj) == type(float()):
            if obj == self.inf:
                return lambda obj: 'Infinity'
            if obj == self.negativeInf:
                return lambda obj: '-Infinity'
            if np.isnan(obj):
                return lambda obj: None
        return super(nanInfPickler, self)._get_flattener(obj)

jsonpickle.pickler.Pickler = nanInfPickler

def fullname(c):
  module = c.__module__
  if module is None or module == str.__class__.__module__:
    return c.__name__
  else:
    return module + '.' + c.__name__

class BaseClass():
    @classmethod
    def fromDict(cls, obj_dict):
        # allowed = ('key1', 'key2')
        # df = {k : v for k, v in d.iteritems() if k in allowed}
        convert_nan(obj_dict)
        return cls(**obj_dict)

    def toDict(self):
        return self.__dict__

    @classmethod
    def fromJson(cls, value):
        # allowed = ('key1', 'key2')
        # df = {k : v for k, v in d.iteritems() if k in allowed}
        json_dict = json.loads(value)
        json_dict['py/object'] = fullname(cls)
        return jsonpickle.decode(json.dumps(json_dict))

    def toJson(self):
        return jsonpickle.encode(self, unpicklable=False)

    @classmethod
    def fromListDict(cls, arr):
        return [cls.fromDict(a) for a in arr]

    @staticmethod
    def toListDict(arr):
        return [a.toDict() for a in arr]

    @classmethod
    def fromListJson(cls, value):
        json_list = json.loads(value)
        for j in json_list:
            j['py/object'] = fullname(cls)
        return jsonpickle.decode(json.dumps(json_list))

    @staticmethod
    def toListJson(arr):
        return jsonpickle.encode(arr, unpicklable=False)