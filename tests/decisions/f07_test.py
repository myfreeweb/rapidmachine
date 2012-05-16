import t

class f07(t.Test):
    
    class TestResource(t.Resource):
        
        encodings = [
            ("identity", lambda x: x),
            ("reverse", lambda x: x[::-1])
        ]
        
        def encodings_provided(self, req, rsp):
            return self.encodings

        def reverse(self, data):
            return data[::-1]

        def to_html(self, req, rsp):
            return "foo"

    def test_no_encodings_provided(self):
        self.TestResource.encodings = None
        self.env.headers['accept-encoding'] = 'reverse'
        self.go()
        self.TestResource.encodings = [
            ('identity', lambda x: x),
            ('reverse', lambda x: x[::-1])
        ]
        
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_encoding, None)
        t.eq(self.rsp.response, 'foo')

    def test_no_acceptable_encoding(self):
        self.env.headers['accept-encoding'] = 'gzip'
        self.go()
        t.eq(self.rsp.status_code, 406)
        t.eq(self.rsp.response, [])

    def test_default(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'foo')
    
    def test_choose_reverse(self):
        self.env.headers['accept-encoding'] = 'reverse'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_encoding, 'reverse')
        t.eq(self.rsp.content_length, 3)
        t.eq(self.rsp.response, 'oof')

    def test_choose_idenity(self):
        self.env.headers['accept-encoding'] = 'identity, reverse;q=0.5'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_encoding, 'identity')
        t.eq(self.rsp.content_length, 3)
        t.eq(self.rsp.response, 'foo')
