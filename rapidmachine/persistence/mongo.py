# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .persistence import Persistence


class MongoPersistence(Persistence):  # pragma: no cover

    "PyMongo persistence adapter"

    def __init__(self, mongo, collection):
        self.db = mongo[collection]

    def create(self, params):
        objid = self.db.insert(params)
        return self.read_one(objid)

    def read_one(self, query, **kwargs):
        d = self.db.find_one(query, **kwargs)
        if d:
            if not "fields" in kwargs:
                kwargs["fields"] = {}
            if "_id" in kwargs["fields"]:
                d["_id"] = str(d["_id"])
            else:
                del d["_id"]
        return d

    def read_many(self, query, **kwargs):
        c = [d for d in self.db.find(query, **kwargs)]
        if not "fields" in kwargs:
            kwargs["fields"] = {}
        if "_id" in kwargs["fields"]:
            for d in c:
                d["_id"] = str(d["_id"])
        else:
            for d in c:
                del d["_id"]
        return c

    def replace(self, query, params):
        self.db.update(query, params)
        return self.read_one(query)

    def update(self, query, params):
        orig = self.read_one(query)
        if not orig:
            return False
        return self.db.update(query, dict(orig.items() + params.items()))

    def delete(self, query):
        return self.db.remove(query)

    def count(self):
        return self.db.count()

__all__ = ["MongoPersistence"]
