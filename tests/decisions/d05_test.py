import t
from should_dsl import *

class d05(t.Test):
    
    class TestResource(t.Resource):
        langs = ["en", "en-gb"]
        
        def languages_provided(self, req, rsp):
            return self.langs

        def to_html(self, req, rsp):
            if rsp.content_language:
                if rsp.content_language[0] == "en-gb":
                    return "Favourite!"
            return "Favorite!"
    
    def test_no_langs(self):
        self.TestResource.langs = None
        self.env.headers["accept-language"] = "en;q=0.3, es"
        self.go()
        self.TestResource.langs = ["en", "en-gb"]
        self.rsp.status_code |should_be.equal_to| 200
        len(self.rsp.content_language) |should_be.equal_to| 0
        self.rsp.response |should_be.equal_to| ["Favorite!"]
    
    def test_none_acceptable(self):
        self.env.headers["accept-language"] = "es"
        self.go()
        self.rsp.status_code |should_be.equal_to| 406
        self.rsp.response |should_be.equal_to| []
    
    def test_en_default(self):
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.response |should_be.equal_to| ["Favorite!"]

    def test_en(self):
        self.env.headers["accept-language"] = "en"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_language[0] |should_be.equal_to| "en"
        self.rsp.response |should_be.equal_to| ["Favorite!"]
    
    def test_en_gb(self):
        self.env.headers["accept-language"] = "en-gb"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_language[0] |should_be.equal_to| "en-gb"
        self.rsp.response |should_be.equal_to| ["Favourite!"]
    
    def test_choose_en(self):
        self.env.headers["accept-language"] = "en;q=0.9, en-gb;q=0.4"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_language[0] |should_be.equal_to| "en"
        self.rsp.response |should_be.equal_to| ["Favorite!"]
