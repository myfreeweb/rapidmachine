import t

class b10(t.Test):
    
    class TestResource(t.Resource):
        
        def allowed_methods(self, req, rsp):
            return ["GET"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ['nom nom'])

    def test_not_ok(self):
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 405)
        t.eq(self.rsp.response, [])
