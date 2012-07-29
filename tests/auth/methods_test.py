import t
from base64 import b64encode
from werkzeug.test import EnvironBuilder
from rapidmachine.exceptions import InvalidAuthException
from rapidmachine.auth.methods import BasicAuthMethod


class FakeAuthBackend(object):

    def get_user(self, username, password):
        return {"username": username, "password": password}


class MethodsTest(t.Test):

    def test_basic_auth_valid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic "+b64encode("usr:pwd")})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), True)
        t.eq(m.get_user(FakeAuthBackend()), {"username": "usr", "password": "pwd"})

    def test_basic_auth_invalid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic notbase64"})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), True)
        t.raises(InvalidAuthException, lambda: m.get_user(FakeAuthBackend()))

    def test_basic_auth_miss(self):
        eb = EnvironBuilder(headers={"Authorization": "Notbasic"})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), False)
