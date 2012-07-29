import t
from base64 import b64encode
from rapidmachine import App, Resource, Route


class AuthInfoResource(Resource):

    def to_html(self, req, rsp):
        if req.user:
            return "Hello, " + req.user["username"]
        else:
            return "Invalid username/password"


class AuthTestApp(App):

    handlers = [
        Route("info").to(AuthInfoResource)
    ]
    auth_backend = t.FakeAuthBackend()


class AppAuthTest(t.Test):

    def setUp(self):
        self.client = AuthTestApp().test_client()

    def test_auth_valid(self):
        t.eq(self.client.get('/info',
            headers={"Authorization": "Basic "+b64encode("usr:pwd")}).data,
            "Hello, usr")

    def test_auth_invalid(self):
        t.eq(self.client.get('/info',
            headers={"Authorization": "Basic notbase64"}).status_code,
            400)
