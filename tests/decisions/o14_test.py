import t
from should_dsl import *

class o14(t.Test):
    
    class TestResource(t.Resource):
        
        conflict = True
        
        def allowed_methods(self, req, rsp):
            return ["PUT"]

        def is_conflict(self, req, rsp):
            return self.conflict

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

        def content_types_accepted(self, req, rsp):
            return [("application/x-www-form-urlencoded", self.from_form)]

        def from_form(self, req, rsp):
            return None

    def test_ok(self):
        self.TestResource.conflict = False
        self.env.method = "PUT"
        self.go()
        self.rsp.status_code |should_be.equal_to| 204
        self.rsp.response |should_be.equal_to| []
    
    def test_conflict(self):
        self.TestResource.conflict = True
        self.env.method = "PUT"
        self.go()
        self.rsp.status_code |should_be.equal_to| 409
        self.rsp.response |should_be.equal_to| []
