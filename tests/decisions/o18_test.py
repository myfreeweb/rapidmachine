import t

class o14(t.Test):
    
    class TestResource(t.Resource):
        
        multiple = True
        
        def allowed_methods(self, req, rsp):
            return ['GET', 'TRACE']
        
        def multiple_choices(self, req, rsp):
            return self.multiple

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_ok(self):
        self.TestResource.multiple = False
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'foo')
    
    def test_multiple(self):
        self.TestResource.multiple = True
        self.go()
        t.eq(self.rsp.status_code, 300)
        t.eq(self.rsp.response, 'foo')

    def test_multiple_no_body(self):
        self.TestResource.multiple = True
        self.env.method = 'TRACE'
        self.go()
        t.eq(self.rsp.status_code, 300)
        t.eq(self.rsp.response, [])
