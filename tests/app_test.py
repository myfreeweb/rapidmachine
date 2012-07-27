import t
from rapidmachine import App, Route, Var, Resource

class TestRes(Resource):
    def to_html(self, req, rsp):
        return "Hi, %s" % req.matches["world"]

class TestApp(App):
    handlers = [
        Route("test_int", Var("world", int)).to(TestRes),
        Route("test_str", Var("world", str)).to(TestRes)
    ]

class AppTest(t.Test):

    def setUp(self):
        self.client = TestApp().test_client()

    def test_vars(self):
        t.eq(self.client.get("/test_int/123").status_code, 200)
        t.eq(self.client.get("/test_int/yay").status_code, 400)
        t.eq(self.client.get("/test_str/yay").status_code, 200)
