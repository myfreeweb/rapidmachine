import t

class n05(t.Test):
    
    class TestResource(t.Resource):
        
        allow = True
        
        def allowed_methods(self, req, rsp):
            return ["POST"]
        
        def allow_missing_post(self, req, rsp):
            return self.allow
        
        def previously_existed(self, req, rsp):
            return True
        
        def process_post(self, req, rsp):
            rsp.response = "processed"
            return True
        
        def resource_exists(self, req, rsp):
            return False
        
        def to_html(self):
            return "Yay"

    def test_allow_post(self):
        self.TestResource.allow = True
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'processed')
    
    def test_dont_allow(self):
        self.TestResource.allow = False
        self.env.method = 'POST'
        self.go()
        t.eq(self.rsp.status_code, 410)
        t.eq(self.rsp.response, [])
