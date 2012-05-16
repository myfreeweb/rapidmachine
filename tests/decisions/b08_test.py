import t

class b08(t.Test):
    
    class TestResource(t.Resource):
        
        def is_authorized(self, req, rsp):
            if req.headers.get('authorization') == 'yay':
                return True
            return 'oauth'

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers['authorization'] = 'yay'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'nom nom')

    def test_not_ok(self):
        self.go()
        t.eq(self.rsp.status_code, 401)
        t.eq(self.rsp.headers['www-authenticate'], 'oauth')
        t.eq(self.rsp.response, [])
