import t

class b05(t.Test):
    
    class TestResource(t.Resource):
        
        def known_content_type(self, req, rsp):
            return req.content_type.split(';')[0] in ["text/plain", "text/xml"]

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.headers['content-type'] = 'text/plain'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ['nom nom'])

    def test_not_ok(self):
        self.env.headers['content-type'] = 'application/json; charset=utf-8'
        self.go()
        t.eq(self.rsp.status_code, 415)
        t.eq(self.rsp.response, [])
