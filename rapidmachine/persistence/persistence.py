# -*- coding: utf-8 -*-


class Persistence(object):

    "Basic persistence interface"

    def __init__(self):
        pass

    def create(self, params):
        raise NotImplemented

    def read_one(self, query):
        raise NotImplemented

    def read_many(self, query):
        raise NotImplemented

    def replace(self, query, params):
        raise NotImplemented

    def update(self, query, params):
        raise NotImplemented

    def delete(self, query):
        raise NotImplemented
