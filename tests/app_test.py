import t
from werkzeug.test import Client
from werkzeug.wrappers import Response
from rapidmachine import App, R, V, Resource

class TestRes(Resource):
    def to_html(self, req, rsp):
        return "Hi, %s" % req.matches['world']

class TestApp(App):
    handlers = [
        R(['test_int', V('world', int)], TestRes),
        R(['test_str', V('world', str)], TestRes)
    ]

class AppTest(t.Test):

    def setUp(self):
        self.client = Client(TestApp(), Response)

    def test_vars(self):
        t.eq(self.client.get('/test_int/123').status_code, 200)
        t.eq(self.client.get('/test_int/yay').status_code, 400)
        t.eq(self.client.get('/test_str/yay').status_code, 200)
