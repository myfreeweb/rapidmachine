import t
from should_dsl import *

class p03(t.Test):
    
    class TestResource(t.Resource):

        def to_html(req, rsp):
            rsp.response = ["bar"]
            return True

        conflict = False
        accepted = [("text/html", to_html)]
        
        def allowed_methods(self, req, rsp):
            return ["PUT"]
        
        def content_types_accepted(self, req, rsp):
            return self.accepted
        
        def is_conflict(self, req, rsp):
            return self.conflict
        
        def moved_permanently(self, req, rsp):
            return False

        def resource_exists(self, req, rsp):
            return False

        def to_html(self, req, rsp):
            return "foo"

    def test_ok(self):
        self.TestResource.conflict = False
        self.env.method = "PUT"
        self.env.content_type = "text/html"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["bar"]
    
    def test_conflict(self):
        self.TestResource.conflict = True
        self.env.method = "PUT"
        self.go()
        self.rsp.status_code |should_be.equal_to| 409
    
    def test_unsupported_media_type(self):
        prev = self.TestResource.accepted
        self.TestResource.accepted = []
        self.TestResource.conflict = False
        self.env.method = "PUT"
        self.go()
        self.TestResource.accepted = prev
        self.rsp.status_code |should_be.equal_to| 415
    
