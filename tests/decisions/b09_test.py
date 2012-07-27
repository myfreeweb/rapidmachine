import t

class b09(t.Test):
    
    class TestResource(t.Resource):
        
        def malformed_request(self, req, rsp):
            try:
                int(req.args.get("value"))
                return False
            except:
                return True

        def to_html(self, req, rsp):
            return "nom nom"
    
    def test_ok(self):
        self.env.query_string = "value=1&foo=true"
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, ["nom nom"])

    def test_not_ok(self):
        self.env.query_string = "value=false"
        self.go()
        t.eq(self.rsp.status_code, 400)
        t.eq(self.rsp.response, [])
