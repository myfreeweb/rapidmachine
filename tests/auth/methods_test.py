import t
from should_dsl import *
from base64 import b64encode
from werkzeug.test import EnvironBuilder
from rapidmachine.exceptions import InvalidAuthException
from rapidmachine.auth.methods import BasicAuthMethod


class MethodsTest(t.Test):

    def test_basic_auth_valid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic "+b64encode("usr:pwd")})
        m = BasicAuthMethod(eb.get_request())
        m.check() |should_be.equal_to| True
        m.get_user(t.FakeAuthBackend()) |should_be.equal_to| {"username": "usr", "password": "pwd"}

    def test_basic_auth_invalid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic notbase64"})
        m = BasicAuthMethod(eb.get_request())
        m.check() |should_be.equal_to| True
        InvalidAuthException |should_be.thrown_by| (lambda: m.get_user(t.FakeAuthBackend()))

    def test_basic_auth_miss(self):
        eb = EnvironBuilder(headers={"Authorization": "Notbasic"})
        m = BasicAuthMethod(eb.get_request())
        m.check() |should_be.equal_to| False
