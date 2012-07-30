import t
from should_dsl import *

class b11(t.Test):
    
    class TestResource(t.Resource):
        
        def uri_too_long(self, req, rsp):
            return len(req.url) > 100

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.path = "/foo" * 40
        self.go()
        self.rsp.status_code |should_be.equal_to| 414
        self.rsp.response |should_be.equal_to| []
