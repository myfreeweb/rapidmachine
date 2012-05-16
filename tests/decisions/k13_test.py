import t

class k13(t.Test):
    
    class TestResource(t.Resource):

        def generate_etag(self, req, rsp):
            return 'foo'

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return 'bar'

    def test_etag_match(self):
        self.env.headers['if-none-match'] = 'foo'
        self.go()
        t.eq(self.rsp.status_code, 304)
        t.eq(self.rsp.etag, 'foo')
        t.eq(self.rsp.response, [])
    
    def test_modified(self):
        self.env.headers['if-none-match'] = 'bar'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.etag, 'foo')
        t.eq(self.rsp.response, ['bar'])
