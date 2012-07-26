# -*- coding: utf-8 -*-

from decisions import process
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from werkzeug.test import Client as TestClient
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
    request_class = Request
    response_class = Response
    not_found_class = NotFound
    test_client_class = TestClient

    def dispatch_response(self, req):
        req.url_object = URLObject(req.url)
        path = req.url_object.path.segments
        for handler in self.handlers:
            route = handler["route"]
            if len(route) == len(path):  # stop early
                try:
                    matches = match(route, path)
                    if matches is not False:
                        rsp = self.response_class()
                        req.matches = matches
                        return process(handler["res"], req, rsp)
                except HTTPException, e:
                    return e
        return self.not_found_class()  # pragma: no cover

    def __call__(self, env, start_rsp):
        req = self.request_class(env)
        rsp = self.dispatch_response(req)
        return rsp(env, start_rsp)

    def devserve(self, port=5000):  # pragma: no cover
        "Starts a development server with this app on a specified port"
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', port, self, use_debugger=True, use_reloader=True)

    def test_client(self, use_cookies=True):
        "Returns a test client for this app"
        return self.test_client_class(self, self.response_class,
                use_cookies=use_cookies)
