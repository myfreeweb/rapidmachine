import t
from should_dsl import *

class b07(t.Test):
    
    class TestResource(t.Resource):
        
        def forbidden(self, req, rsp):
            return req.cookies.get("id") != "foo"

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers["cookie"] = "id=foo"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.headers["cookie"] = "bar"
        self.go()
        self.rsp.status_code |should_be.equal_to| 403
        self.rsp.response |should_be.equal_to| []
