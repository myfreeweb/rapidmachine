# -*- coding: utf-8 -*-

from persistence import Persistence

class MemoryPersistence(Persistence):
    "In-memory list persistence adapter, ONLY FOR DEVELOPMENT"

    def __init__(self):
        self.db = []

    def matches(self, d, query):
        for key, qval in query.iteritems():
            dval = d[key]
            if type(dval) != type(qval):
                return False
            if type(dval) == dict and not self.matches(dval, qval):
                return False
            if dval != qval:
                return False
        return True

    def create(self, params):
        return self.db.append(params)

    def read_many(self, query):
        return filter(lambda d: self.matches(d, query), self.db)

    def read_one(self, query):
        try:
            return self.read_many(query)[0]
        except IndexError:
            return None

    def replace(self, query, params):
        self.db = map(lambda d: params if self.matches(d, query) else d, self.db)
        # who cares about performance there? it's for development
        return self.read_one(query)

    def update(self, query, params):
        self.db = map(lambda d: dict(d.items() + params.items()) if
                self.matches(d, query) else d, self.db)
        # who cares about performance there? it's for development
        return self.read_one(query)

    def delete(self, query):
        self.db = filter(lambda d: not self.matches(d, query), self.db)
