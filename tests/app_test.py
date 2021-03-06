import t
from should_dsl import *
from rapidmachine import App, Route, Var, Resource


class TestRes(Resource):

    def to_html(self, req, rsp):
        return "Hi, %s" % req.matches["world"]


class TestOverrideRes(Resource):

    def allowed_methods(self, req, rsp):
        return ["GET", "HEAD", "POST", "PUT"]

    def from_text(self, req, rsp):
        rsp.headers["X-Method"] = req.method

    def to_html(self, req, rsp):
        return req.method + " " + req.headers["Accept"]

    def content_types_provided(self, req, rsp):
        return [
            ("text/html", self.to_html),
            ("text/plain", self.to_html)
        ]

    def content_types_accepted(self, req, rsp):
        return [ ("text/plain", self.from_text) ]


class TestApp(App):
    handlers = [
        Route("test").to(TestOverrideRes),
        Route("test_int", Var("world", int)) >> TestRes,
        Route("test_str", Var("world", str)).to(TestRes)
    ]


class AppTest(t.Test):

    def setUp(self):
        self.client = TestApp().test_client()

    def test_vars(self):
        self.client.get("/test_int/123").status_code |should_be.equal_to| 200
        self.client.get("/test_int/yay").status_code |should_be.equal_to| 400
        self.client.get("/test_str/yay").status_code |should_be.equal_to| 200

    def test_override(self):
        self.client.get("/test", headers={"Accept": "text/html"}).data \
                |should_be.equal_to| "GET text/html"
        self.client.post("/test?_method=put", content_type="text/plain")\
                .headers["X-Method"] |should_be.equal_to| "PUT"
