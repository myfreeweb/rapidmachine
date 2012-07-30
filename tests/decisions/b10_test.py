import t
from should_dsl import *

class b10(t.Test):
    
    class TestResource(t.Resource):
        
        def allowed_methods(self, req, rsp):
            return ["GET"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.method = "POST"
        self.go()
        self.rsp.status_code |should_be.equal_to| 405
        self.rsp.response |should_be.equal_to| []
