# -*- coding: utf-8 -*-
from base64 import b64decode
from rapidmachine.exceptions import InvalidAuthException


class AuthMethod(object):
    """
    Basic auth method.

    All methods here (except __init__) just raise NotImplemented.
    Use one of its subclasses or make your own.
    """

    def __init__(self, req):
        self.req = req

    def check(self):
        """
        Returns whether the request can be authorized using this method (a
        boolean).
        """
        raise NotImplemented

    def get_user(self, backend):
        """
        Extracts the username and password from the request and calls get_user
        on backend with them.
        """
        raise NotImplemented


class BasicAuthMethod(AuthMethod):
    """
    Auth method that implements HTTP Basic authentication.
    """

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
