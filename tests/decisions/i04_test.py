import t
from should_dsl import *

class i04(t.Test):
    
    class TestResource(t.Resource):

        moved = False
        
        def allowed_methods(self, req, rsp):
            return ["PUT"]
        
        def content_types_accepted(self, req, rsp):
            return [("text/html", self.from_html)]
        
        def moved_permanently(self, req, rsp):
            return self.moved

        def resource_exists(self, req, rsp):
            return False

        def from_html(self, req, rsp):
            rsp.response = ["bar"]

        def to_html(self, req, rsp):
            return "foo"

    def test_not_moved(self):
        self.TestResource.moved = False
        self.env.method = "PUT"
        self.env.content_type = "text/html"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["bar"]
    
    def test_moved(self):
        self.TestResource.moved = "/foo"
        self.env.method = "PUT"
        self.go()
        self.rsp.status_code |should_be.equal_to| 301
        self.rsp.location |should_be.equal_to| "/foo"
