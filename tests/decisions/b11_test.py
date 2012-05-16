import t

class b11(t.Test):
    
    class TestResource(t.Resource):
        
        def uri_too_long(self, req, rsp):
            return len(req.url) > 100

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'nom nom')

    def test_not_ok(self):
        self.env.path = '/foo' * 40
        self.go()
        t.eq(self.rsp.status_code, 414)
        t.eq(self.rsp.response, [])
