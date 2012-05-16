import t

class n11(t.Test):
    
    class TestResource(t.Resource):
        
        create = False
        status = True
        location = '/foo'
        
        def allowed_methods(self, req, rsp):
            return ["POST"]
        
        def allow_missing_post(self, req, rsp):
            return True
        
        def content_types_accepted(self, req, rsp):
            return [('application/octet-stream', self.from_octets)]
        
        def created_location(self, req, rsp):
            return self.location
        
        def post_is_create(self, req, rsp):
            return self.create
        
        def process_post(self, req, rsp):
            if not self.create:
                rsp.response = "processed"
            return self.status
        
        def resource_exists(self, req, rsp):
            return False
        
        def from_octets(self, req, rsp):
            rsp.response = "created"
        
        def to_html(self, req, rsp):
            return "Yay"

    def test_post_is_create_no_redirect(self):
        self.TestResource.create = True
        self.TestResource.location = None
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'created')

    def test_post_is_create_redirect(self):
        self.TestResource.create = True
        self.TestResource.location = '/foo'
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 303)
        t.eq(self.rsp.headers.get('location'), '/foo')
        t.eq(self.rsp.response, 'created')

    def test_post_is_process(self):
        self.TestResource.create = False
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.headers.get('location'), None)
        t.eq(self.rsp.response, 'processed')
    
    def test_post_is_process_error(self):
        self.TestResource.create = False
        self.TestResource.status = False
        self.env.method = 'POST'
        self.go()
        self.TestResource.status = True
        t.eq(self.rsp.status_code, 500)
        t.eq(self.rsp.headers.get('location'), None)
