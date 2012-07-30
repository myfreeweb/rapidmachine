import t
from should_dsl import *

class g11(t.Test):
    
    class TestResource(t.Resource):
        
        def generate_etag(self, req, rsp):
            return "bar"

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_no_if_match(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.etag |should_be.equal_to| "bar"
        self.rsp.response |should_be.equal_to| ["foo"]
    
    def test_if_match_ok(self):
        self.env.headers["if-match"] = "bar"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.etag |should_be.equal_to| "bar"
        self.rsp.response |should_be.equal_to| ["foo"]
    
    def test_if_match_fail(self):
        self.env.headers["if-match"] = "baz"
        self.go()
        self.rsp.status_code |should_be.equal_to| 412
        self.rsp.response |should_be.equal_to| []
