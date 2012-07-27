import t

class g07(t.Test):
    
    class TestResource(t.Resource):

        exists = True

        def content_types_provided(self, req, rsp):
            return [
                ("text/html", self.to_html),
                ("text/plain", self.to_plain)
            ]
        
        def languages_provided(self, req, rsp):
            return ["en", "en-gb", "es"]
        
        def resource_exists(self, req, rsp):
            return self.exists
        
        def variances(self, req, rsp):
            return ["Cookie"]

        def to_html(self, req, rsp):
            return "<html><body>foo</body></html>"
        
        def to_plain(self, req, rsp):
            return "foo"

    def test_variances(self):
        self.TestResource.exists = True
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(sorted(self.rsp.vary), ["Accept", "Accept-Language", "Cookie"])

    def test_resource_not_exists(self):
        self.TestResource.exists = False
        self.go()
        t.eq(self.rsp.status_code, 404)
        t.eq(self.rsp.response, [])
        
