import t

class b04(t.Test):
    
    class TestResource(t.Resource):
        
        def valid_entity_length(self, req, rsp):
            return req.content_length < 1024

        def to_html(self, req, rsp):
            return "yay good"
    
    def test_ok(self):
        self.env.data = 'foo'
        self.env.headers['content-length'] = len(self.env.data)
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ['yay good'])

    def test_not_ok(self):
        self.env.data = 'foo' * 1024
        self.env.headers['content-length'] = len(self.env.data)
        self.go()
        t.eq(self.rsp.status_code, 413)
        t.eq(self.rsp.response, [])
