# -*- coding: utf-8 -*-

from decisions import process
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from urlobject import URLObject


class Var(object):

    def __init__(self, name, typey=str):
        assert type(typey) == type
        self.name = name
        self.typey = typey


class Route(object):

    def __init__(self, *args):
        self.route = args

    def to(self, res):
        return {"route": self.route, "res": res}


def match(route, path):
    "Match a path against a route. Returns a dict of values or False."
    matches = {}
    for routepart, pathpart in zip(route, path):
        if routepart != pathpart and routepart != "*":
            if isinstance(routepart, Var):
                try:
                    matches[routepart.name] = routepart.typey(pathpart)
                except ValueError:  # wrong type
                    raise BadRequest()
            else:  # didn't match
                return False
    return matches


class App(object):

    """
    A WSGI application which routes requests to Resources.

    This class is meant to be subclassed. Usage:
    Set the handlers attribute to a list of routes, initialize and pass to a
    WSGI server.
    """

    handlers = []

    def dispatch_response(self, req):
        req.url_object = URLObject(req.url)
        path = req.url_object.path.segments
        for handler in self.handlers:
            route = handler["route"]
            if len(route) == len(path):  # stop early
                try:
                    matches = match(route, path)
                    if matches is not False:
                        rsp = Response()
                        req.matches = matches
                        return process(handler["res"], req, rsp)
                except HTTPException, e:
                    return e
        return NotFound()  # pragma: no cover

    def __call__(self, env, start_rsp):
        req = Request(env)
        rsp = self.dispatch_response(req)
        return rsp(env, start_rsp)

    def devserve(self, port=5000):  # pragma: no cover
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', port, self, use_debugger=True, use_reloader=True)
