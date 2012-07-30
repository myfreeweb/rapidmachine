import unittest
from werkzeug.wrappers import Request, Response
from werkzeug.test import EnvironBuilder
from werkzeug.exceptions import HTTPException
from rapidmachine import Resource
from rapidmachine.decisions import process


class Test(unittest.TestCase):
    def setUp(self):
        self.env = EnvironBuilder()
        self.rsp = Response()

    def go(self):
        environ = self.env.get_environ()
        try:
            self.req = Request(environ)
            process(self.TestResource, self.req, self.rsp)
        except HTTPException, error:
            self.rsp = error.get_response(environ)


class FakeAuthBackend(object):

    def get_user(self, username, password):
        return {"username": username, "password": password}
