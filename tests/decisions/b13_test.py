import t
from should_dsl import *

class b13(t.Test):

    class TestResource(t.Resource):

        available = True
        pong = True

        def ping(self, req, rsp):
            print self.pong
            return self.pong

        def service_available(self, req, rsp):
            print self.available
            return self.available

        def to_html(self, req, rsp):
            return "nom nom"

    def test_ok(self):
        self.TestResource.available = True
        self.TestResource.pong = True
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["nom nom"]

    def test_no_service(self):
        self.TestResource.available = False
        self.TestResource.pong = True
        self.go()
        self.rsp.status_code |should_be.equal_to| 503
        self.rsp.response |should_be.equal_to| []
