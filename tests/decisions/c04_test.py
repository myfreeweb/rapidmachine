import t

class c04(t.Test):
    
    class TestResource(t.Resource):
        
        def content_types_provided(self, req, rsp):
            return [
                ('application/json', self.to_json),
                ('text/xml', self.to_xml)
            ]

        def to_json(self, req, rsp):
            return '{"nom": "nom"}'

        def to_xml(self, req, rsp):
            return "<nom>nom</nom>"

    def test_no_accept(self):
        # No Accept header means default to first specified.
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.response, '{"nom": "nom"}')

    def test_none_acceptable(self):
        self.env.headers['accept'] = 'image/jpeg'
        self.go()
        t.eq(self.rsp.status_code, 406)

    def test_json(self):
        self.env.headers['accept'] = 'application/json'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.response, '{"nom": "nom"}')

    def test_xml(self):
        self.env.headers['accept'] = 'text/xml'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_type, 'text/xml')
        t.eq(self.rsp.response, '<nom>nom</nom>')
    
    def test_choose_best(self):
        self.env.headers['accept'] = 'text/xml;q=0.5, application/json;q=0.9'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_type, 'application/json')
        t.eq(self.rsp.response, '{"nom": "nom"}')
