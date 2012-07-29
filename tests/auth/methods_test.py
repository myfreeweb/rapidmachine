import t
from base64 import b64encode
from werkzeug.test import EnvironBuilder
from rapidmachine.exceptions import InvalidAuthException
from rapidmachine.auth.methods import BasicAuthMethod


class MethodsTest(t.Test):

    def test_basic_auth_valid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic "+b64encode("usr:pwd")})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), True)
        t.eq(m.get_user(t.FakeAuthBackend()), {"username": "usr", "password": "pwd"})

    def test_basic_auth_invalid(self):
        eb = EnvironBuilder(headers={"Authorization": "Basic notbase64"})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), True)
        t.raises(InvalidAuthException, lambda: m.get_user(t.FakeAuthBackend()))

    def test_basic_auth_miss(self):
        eb = EnvironBuilder(headers={"Authorization": "Notbasic"})
        m = BasicAuthMethod(eb.get_request())
        t.eq(m.check(), False)
