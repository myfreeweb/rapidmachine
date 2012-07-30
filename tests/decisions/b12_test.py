import t
from should_dsl import *

class b12(t.Test):
    
    class TestResource(t.Resource):
        
        def known_methods(self, req, rsp):
            return ["GET"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.method = "PUT"
        self.go()
        self.rsp.status_code |should_be.equal_to| 501
        self.rsp.response |should_be.equal_to| []
