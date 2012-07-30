import t
from should_dsl import *

class g07(t.Test):
    
    class TestResource(t.Resource):

        exists = True

        def content_types_provided(self, req, rsp):
            return [
                ("text/html", self.to_html),
                ("text/plain", self.to_plain)
            ]
        
        def languages_provided(self, req, rsp):
            return ["en", "en-gb", "es"]
        
        def resource_exists(self, req, rsp):
            return self.exists
        
        def variances(self, req, rsp):
            return ["Cookie"]

        def to_html(self, req, rsp):
            return "<html><body>foo</body></html>"
        
        def to_plain(self, req, rsp):
            return "foo"

    def test_variances(self):
        self.TestResource.exists = True
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        sorted(self.rsp.vary) |should_be.equal_to| ["Accept", "Accept-Language", "Cookie"]

    def test_resource_not_exists(self):
        self.TestResource.exists = False
        self.go()
        self.rsp.status_code |should_be.equal_to| 404
        self.rsp.response |should_be.equal_to| []
        
