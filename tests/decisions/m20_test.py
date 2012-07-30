import t
from should_dsl import *

class g11(t.Test):
    
    class TestResource(t.Resource):
        
        done = True
        
        def allowed_methods(self, req, rsp):
            return ["DELETE"]

        def delete_completed(self, req, rsp):
            return self.done

        def delete_resource(self, req, rsp):
            return True

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_done(self):
        self.TestResource.done = True
        self.env.method = "DELETE"
        self.go()
        self.rsp.status_code |should_be.equal_to| 204
        self.rsp.response |should_be.equal_to| []
    
    def test_not_done(self):
        self.TestResource.done = False
        self.env.method = "DELETE"
        self.go()
        self.rsp.status_code |should_be.equal_to| 202
        self.rsp.response |should_be.equal_to| []
