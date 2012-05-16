import t

class b07(t.Test):
    
    class TestResource(t.Resource):
        
        def forbidden(self, req, rsp):
            return req.cookies.get('id') != 'foo'

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers['cookie'] = 'id=foo'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ['nom nom'])

    def test_not_ok(self):
        self.env.headers['cookie'] = 'bar'
        self.go()
        t.eq(self.rsp.status_code, 403)
        t.eq(self.rsp.response, [])
