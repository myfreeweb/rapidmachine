import t
from should_dsl import *

class k07(t.Test):
    
    class TestResource(t.Resource):

        existed = False
        
        def previously_existed(self, req, rsp):
            return self.existed

        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_not_existed(self):
        self.TestResource.existed = False
        self.go()
        self.rsp.status_code |should_be.equal_to| 404
        self.rsp.response |should_be.equal_to| []
    
    def test_existed(self):
        self.TestResource.existed = True
        self.go()
        self.rsp.status_code |should_be.equal_to| 410
        self.rsp.response |should_be.equal_to| []
