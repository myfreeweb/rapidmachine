import datetime
from should_dsl import *
import t

now = datetime.datetime.utcnow().replace(microsecond=0)
diff = datetime.timedelta(days=1)
past = now - diff
future = now + diff

class h12(t.Test):
    
    class TestResource(t.Resource):

        modified = now
        
        def last_modified(self, req, rsp):
            return self.modified

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_unmodified(self):
        self.env.headers["if-unmodified-since"] = future.ctime()
        self.go()
        self.rsp.status_code |should_be.equal_to| 200
        self.rsp.last_modified |should_be.equal_to| now
        self.rsp.response |should_be.equal_to| ["foo"]
    
    def test_modified(self):
        self.env.headers["if-unmodified-since"] = past.ctime()
        self.go()
        self.rsp.status_code |should_be.equal_to| 412
