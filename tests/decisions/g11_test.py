import t

class g11(t.Test):
    
    class TestResource(t.Resource):
        
        def generate_etag(self, req, rsp):
            return "bar"

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_no_if_match(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.etag, 'bar')
        t.eq(self.rsp.response, ['foo'])
    
    def test_if_match_ok(self):
        self.env.headers['if-match'] = 'bar'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.etag, 'bar')
        t.eq(self.rsp.response, ['foo'])
    
    def test_if_match_fail(self):
        self.env.headers['if-match'] = 'baz'
        self.go()
        t.eq(self.rsp.status_code, 412)
        t.eq(self.rsp.response, [])
