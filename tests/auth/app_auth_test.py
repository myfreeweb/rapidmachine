import t
from should_dsl import *
from base64 import b64encode
from rapidmachine import App, Resource, Route


class AuthInfoResource(Resource):

    def to_html(self, req, rsp):
        if req.user:
            return "Hello, " + req.user["username"]
        else:
            return "No auth"


class AuthTestApp(App):

    handlers = [
        Route("info").to(AuthInfoResource)
    ]
    auth_backend = t.FakeAuthBackend()


class AppAuthTest(t.Test):

    def setUp(self):
        self.client = AuthTestApp().test_client()

    def test_auth_valid(self):
        self.client.get('/info', headers={"Authorization": "Basic "+\
                b64encode("usr:pwd")}).data |should_be.equal_to| "Hello, usr"

    def test_auth_invalid(self):
        self.client.get('/info', headers={"Authorization": "Basic notb64"})\
                .status_code |should_be.equal_to| 400

    def test_no_auth(self):
        self.client.get('/info').data |should_be.equal_to| "No auth"
