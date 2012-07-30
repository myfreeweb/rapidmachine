import t
from should_dsl import *

class b03(t.Test):
    
    class TestResource(t.Resource):
        def allowed_methods(self, req, rsp):
            return ["GET", "OPTIONS"]

        def options(self, req, rsp):
            return [("X-Noah", "Awesome")]

        def to_html(self, req, rsp):
            return "Hello, world!"

    def test_get(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.headers.get("X-Noah") |should_be.equal_to| None
        self.rsp.response |should_be.equal_to| ["Hello, world!"]

    def test_options(self):
        self.env.method = "OPTIONS"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.headers["X-Noah"] |should_be.equal_to| "Awesome"
        self.rsp.response |should_be.equal_to| []

    # Fairly unrelated, but no good place to put this
    def test_non_unicode_body(self):
        prev = self.TestResource.to_html
        def my_html(self, req, rsp):
            rsp.charset = None
            return "Hi"
        self.TestResource.to_html = my_html
        self.go()
        self.TestResource.to_html = prev
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["Hi"]
