import unittest
from werkzeug.wrappers import Request, Response
from werkzeug.test import EnvironBuilder
from werkzeug.exceptions import HTTPException
from rapidmachine import process, Resource

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

def eq(a, b):
    assert a == b, "%r != %r" % (a, b)

def ne(a, b):
    assert a != b, "%r == %r" % (a, b)

def lt(a, b):
    assert a < b, "%r >= %r" % (a, b)

def gt(a, b):
    assert a > b, "%r <= %r" % (a, b)

def isin(a, b):
    assert a in b, "%r is not in %r" % (a, b)

def isnotin(a, b):
    assert a not in b, "%r is in %r" % (a, b)

def has(a, b):
    assert hasattr(a, b), "%r has no attribute %r" % (a, b)

def hasnot(a, b):
    assert not hasattr(a, b), "%r has an attribute %r" % (a, b)

def raises(exctype, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exctype, inst:
        pass
    else:
        func_name = getattr(func, "func_name", "<builtin_function>")
        raise AssertionError("Function %s did not raise %s" % (
            func_name, exctype.__name__))

