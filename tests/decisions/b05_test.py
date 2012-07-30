import t
from should_dsl import *

class b05(t.Test):
    
    class TestResource(t.Resource):
        
        def known_content_type(self, req, rsp):
            return req.content_type.split(";")[0] in ["text/plain", "text/xml"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers["content-type"] = "text/plain"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.headers["content-type"] = "application/json; charset=utf-8"
        self.go()
        self.rsp.status_code |should_be.equal_to| 415
        self.rsp.response |should_be.equal_to| []
