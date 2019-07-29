# -*- coding: utf-8 -*-

import json
import jsonpickle
import msgpack

def fullname(c):
  module = c.__module__
  if module is None or module == str.__class__.__module__:
    return c.__name__
  else:
    return module + '.' + c.__name__

class BaseClass():
    @classmethod
    def fromDict(cls, dict):
        # allowed = ('key1', 'key2')
        # df = {k : v for k, v in d.iteritems() if k in allowed}
        return cls(**dict)

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
