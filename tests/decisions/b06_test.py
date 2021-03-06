import t
from should_dsl import *

class b06(t.Test):
    
    class TestResource(t.Resource):
        
        def valid_content_headers(self, req, rsp):
            if req.headers.get("content-foo"):
                return False
            return True

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers["content-type"] = "text/plain"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.headers["content-foo"] = "bizbang"
        self.go()
        self.rsp.status_code |should_be.equal_to| 501
