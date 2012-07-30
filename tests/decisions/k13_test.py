import t
from should_dsl import *

class k13(t.Test):
    
    class TestResource(t.Resource):

        def generate_etag(self, req, rsp):
            return "foo"

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "bar"

    def test_etag_match(self):
        self.env.headers["if-none-match"] = "foo"
        self.go()
        self.rsp.status_code |should_be.equal_to| 304
        self.rsp.etag |should_be.equal_to| "foo"
        self.rsp.response |should_be.equal_to| []
    
    def test_modified(self):
        self.env.headers["if-none-match"] = "bar"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.etag |should_be.equal_to| "foo"
        self.rsp.response |should_be.equal_to| ["bar"]
