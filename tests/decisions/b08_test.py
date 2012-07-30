import t
from should_dsl import *

class b08(t.Test):
    
    class TestResource(t.Resource):
        
        def is_authorized(self, req, rsp):
            if req.headers.get("authorization") == "yay":
                return True
            return "oauth"

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers["authorization"] = "yay"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 401
        self.rsp.headers["www-authenticate"] |should_be.equal_to| "oauth"
        self.rsp.response |should_be.equal_to| []
