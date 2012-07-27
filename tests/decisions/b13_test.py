import t

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
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ["nom nom"])

    def test_no_service(self):
        self.TestResource.available = False
        self.TestResource.pong = True
        self.go()
        t.eq(self.rsp.status_code, 503)
        t.eq(self.rsp.response, [])
