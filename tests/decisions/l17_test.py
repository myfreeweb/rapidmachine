import datetime
import t

now = datetime.datetime.utcnow().replace(microsecond=0)
diff = datetime.timedelta(days=1)
past = now - diff
future = now + diff

class l17(t.Test):
    
    class TestResource(t.Resource):

        modified = now
        
        def last_modified(self, req, rsp):
            return self.modified

        def resource_exists(self, req, rsp):
            return True

        def to_html(self, req, rsp):
            return "foo"

    def test_unmodified(self):
        self.TestResource.modified = now
        self.env.headers['if-modified-since'] = past
        self.go()
        t.eq(self.rsp.status_code, 200)
        t.eq(self.rsp.last_modified, now)
        t.eq(self.rsp.response, 'foo')
    
    def test_modified(self):
        self.TestResource.modified = past
        self.env.headers['if-modified-since'] = now
        self.go()
        t.eq(self.rsp.status_code, 304)
