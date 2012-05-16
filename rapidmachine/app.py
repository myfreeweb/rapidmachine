# -*- coding: utf-8 -*-

from decisions import process
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from urlobject import URLObject

class V(object):
    def __init__(self, name, typey):
        assert type(typey) == type
        self.name = name
        self.typey = typey

def R(route, res):
    return {"route": route, "res": res}

def match(route, path):
    matches = {}
    for routepart, pathpart in zip(route, path):
        if routepart != pathpart and routepart != "*":
            if type(routepart) == V:
                try:
                    matches[routepart.name] = routepart.typey(pathpart)
                except ValueError, e:
                    raise BadRequest()
            else:
                return False
    return matches

class App(object):

    handlers = []

    def dispatch_response(self, req):
        path = URLObject(req.path).path.segments
        print path
        for handler in self.handlers:
            route = handler["route"]
            if len(route) == len(path): # stop early
                try:
                    matches = match(route, path)
                    if matches != False:
                        rsp = Response()
                        req.matches = matches
                        return process(handler["res"], req, rsp)
                except HTTPException, e:
                    return e
        return NotFound()

    def __call__(self, env, start_rsp):
        req = Request(env)
        rsp = self.dispatch_response(req)
        return rsp(env, start_rsp)
