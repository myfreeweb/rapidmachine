import t

class e06(t.Test):
    
    class TestResource(t.Resource):
        charsets = ["UTF-8", "iso-8859-1"]
        
        def charsets_provided(self, req, rsp):
            return self.charsets

        def to_html(self, req, rsp):
            if rsp.charset == 'UTF-8':
                return "unicode!"
            else:
                return "ascii!"
    
    def test_no_charsets(self):
        self.TestResource.charsets = None
        self.env.headers['accept-charset'] = 'iso-8859-1'
        self.go()
        self.TestResource.charsets = ['utf-8', 'iso-8859-1']
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.charset, None)
        t.eq(self.rsp.response, ['ascii!'])
    
    def test_none_acceptable(self):
        self.TestResource.charsets = ['utf-8']
        self.env.headers['accept-charset'] = 'latin-1'
        self.go()
        self.TestResource.charsets = ['utf-8', 'iso-8859-1']
        print self.rsp.charset
        t.eq(self.rsp.status_code, 406)
        t.eq(self.rsp.response, [])
    
    def test_default(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.charset, None)
        t.eq(self.rsp.response, ['ascii!'])

    def test_choose_utf_8(self):
        self.env.headers['accept-charset'] = 'utf-8'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.charset, 'UTF-8')
        t.eq(self.rsp.response, ['unicode!'])

    def test_choose_iso_8859_1(self):
        self.env.headers['accept-charset'] = 'iso-8859-1;q=0.8, utf-8;q=0.2'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.charset, 'iso-8859-1')
        t.eq(self.rsp.response, ['ascii!'])
