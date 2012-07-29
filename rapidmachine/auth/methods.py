# -*- coding: utf-8 -*-
from base64 import b64decode
from rapidmachine.exceptions import InvalidAuthException


class AuthMethod(object):

    def __init__(self, req):
        self.req = req

    def check(self):
        raise NotImplemented

    def get_user(self, backend):
        raise NotImplemented

class BasicAuthMethod(AuthMethod):

    def check(self):
        h = self.req.headers["Authorization"]
        if h:
            return h[:5] == "Basic"
        return False

    def get_user(self, backend):
        try:
            data = b64decode(self.req.headers["Authorization"][6:]).split(":")
        except TypeError:
            raise InvalidAuthException
        return backend.get_user(data[0], data[1])
