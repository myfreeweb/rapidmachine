import t
from should_dsl import *

class l05(t.Test):
    
    class TestResource(t.Resource):

        moved = False
        
        def moved_temporarily(self, req, rsp):
            return self.moved

        def previously_existed(self, req, rsp):
            return True

        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_not_moved(self):
        self.TestResource.moved = False
        self.go()
        self.rsp.status_code |should_be.equal_to| 410
        self.rsp.response |should_be.equal_to| []
    
    def test_moved(self):
        self.TestResource.moved = "/foo"
        self.go()
        self.rsp.status_code |should_be.equal_to| 307
        self.rsp.location |should_be.equal_to| "/foo"
        self.rsp.response |should_be.equal_to| []
