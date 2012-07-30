import t
from should_dsl import *

class b09(t.Test):
    
    class TestResource(t.Resource):
        
        def malformed_request(self, req, rsp):
            try:
                int(req.args.get("value"))
                return False
            except:
                return True

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.query_string = "value=1&foo=true"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_not_ok(self):
        self.env.query_string = "value=false"
        self.go()
        self.rsp.status_code |should_be.equal_to| 400
        self.rsp.response |should_be.equal_to| []
