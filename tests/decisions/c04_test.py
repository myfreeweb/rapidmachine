import t
from should_dsl import *

class c04(t.Test):
    
    class TestResource(t.Resource):
        
        def content_types_provided(self, req, rsp):
            return [
                ("application/json", self.to_json),
                ("text/xml", self.to_xml)
            ]

        def to_json(self, req, rsp):
            return '{"nom": "nom"}'

        def to_xml(self, req, rsp):
            return "<nom>nom</nom>"

    def test_no_accept(self):
        # No Accept header means default to first specified.
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_type |should_be.equal_to| "application/json"
        self.rsp.response |should_be.equal_to| ['{"nom": "nom"}']

    def test_none_acceptable(self):
        self.env.headers["accept"] = "image/jpeg"
        self.go()
        self.rsp.status_code |should_be.equal_to| 406

    def test_json(self):
        self.env.headers["accept"] = "application/json"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_type |should_be.equal_to| "application/json"
        self.rsp.response |should_be.equal_to| ['{"nom": "nom"}']

    def test_xml(self):
        self.env.headers["accept"] = "text/xml"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_type |should_be.equal_to| "text/xml"
        self.rsp.response |should_be.equal_to| ["<nom>nom</nom>"]
    
    def test_choose_best(self):
        self.env.headers["accept"] = "text/xml;q=0.5, application/json;q=0.9"
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.content_type |should_be.equal_to| "application/json"
        self.rsp.response |should_be.equal_to| ['{"nom": "nom"}']
