import t

class d05(t.Test):
    
    class TestResource(t.Resource):
        langs = ["en", "en-gb"]
        
        def languages_provided(self, req, rsp):
            return self.langs

        def to_html(self, req, rsp):
            if rsp.content_language:
                if rsp.content_language[0] == 'en-gb':
                    return "Favourite!"
            return "Favorite!"
    
    def test_no_langs(self):
        self.TestResource.langs = None
        self.env.headers['accept-language'] = 'en;q=0.3, es'
        self.go()
        self.TestResource.langs = ['en', 'en-gb']
        t.eq(self.rsp.status_code, 200)
        t.eq(len(self.rsp.content_language), 0)
        t.eq(self.rsp.response, 'Favorite!')
    
    def test_none_acceptable(self):
        self.env.headers['accept-language'] = 'es'
        self.go()
        t.eq(self.rsp.status_code, 406)
        t.eq(self.rsp.response, [])
    
    def test_en_default(self):
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.response, 'Favorite!')

    def test_en(self):
        self.env.headers['accept-language'] = 'en'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_language[0], 'en')
        t.eq(self.rsp.response, 'Favorite!')
    
    def test_en_gb(self):
        self.env.headers['accept-language'] = 'en-gb'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_language[0], 'en-gb')
        t.eq(self.rsp.response, 'Favourite!')
    
    def test_choose_en(self):
        self.env.headers['accept-language'] = 'en;q=0.9, en-gb;q=0.4'
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.content_language[0], 'en')
        t.eq(self.rsp.response, 'Favorite!')
