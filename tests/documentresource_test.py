import t
try:
    import json
except ImportError: # Python 2.5
    import simplejson as json
from werkzeug.test import Client
from werkzeug.wrappers import Response
from rapidmachine import App, Route, Var, DocumentResource
from rapidmachine.persistence import MemoryPersistence
from dictshield.document import Document
from dictshield.fields import StringField


ajson = {'Accept': 'application/json'}
hjson = {'Accept': 'application/hal+json'}
mp = MemoryPersistence()


class Post(Document):
    _public_fields = ['title', 'body']
    title = StringField(max_length=64)
    body  = StringField(max_length=1024)


class PostResource(DocumentResource):
    document    = Post
    persistence = mp
    pk          = 'title'

    def default_per_page(self, req, rsp):
        return 5


class TestApp(App):
    handlers = [
        Route('posts').to(PostResource),
        Route('posts', Var('title', str)).to(PostResource),
        Route('posts.schema').to(PostResource.schema_resource()),
    ]


class AppTest(t.Test):

    def setUp(self):
        self.client = Client(TestApp(), Response)

    def test_create_valid(self):
        rsp = self.client.post('/posts', content_type='application/json',
                data='{"title":"Hello","body":"Hello World!"}')
        t.eq(rsp.headers['location'], 'http://localhost/posts/Hello')

    def test_create_invalid_format(self):
        rsp = self.client.post('/posts', content_type='application/json',
                data='{"title":Hello""body":"Hello!"')
        t.eq(rsp.status_code, 400)

    def test_create_invalid_data(self):
        rsp = self.client.post('/posts', content_type='application/json',
                data='{"title":"%s","body":"Hello World!"}' % ('Hello' * 128))
        t.eq(rsp.status_code, 422)
        t.eq(json.loads(rsp.data)["errors"], {"title": ["String value is too long"]})

    def test_read_valid(self):
        rsp = self.client.get('/posts/Hello', headers=ajson)
        t.eq(rsp.status_code, 200)
        t.eq(json.loads(rsp.data), {"title": "Hello", "body": "Hello World!"})

        rsp = self.client.get('/posts/Hello', headers=hjson)
        t.eq(json.loads(rsp.data), {
            "_links": {"self": {"href": "/posts/Hello"}},
            "title": "Hello",
            "body": "Hello World!"
        })


    def test_read_index(self):
        rsp = self.client.get('/posts', headers=ajson)
        t.eq(rsp.status_code, 200)
        t.eq(json.loads(rsp.data), [{"title": "Hello", "body": "Hello World!"}])

        rsp = self.client.get('/posts', headers=hjson)
        t.eq(json.loads(rsp.data), {
            "_links": {"self": {"href": "/posts"}},
            "_embedded": {
                "post": [
                    {
                        "_links": {"self": {"href": "/posts/Hello"}},
                        "title": "Hello",
                        "body": "Hello World!"
                    }
                ]
            }
        })

    def test_read_invalid(self):
        rsp = self.client.get('/posts/Goodbye', headers=ajson)
        t.eq(rsp.status_code, 404)

    def test_read_schema(self):
        rsp = self.client.get('/posts.schema', headers=ajson)
        t.eq(json.loads(rsp.data)['type'], 'object')
        t.eq(rsp.status_code, 200)

    def test_read_paginated(self):
        for n in range(0, 11):
            mp.create({'title': 'yo', 'body': 'Hello' * n})

        # Happy cases
        rsp = self.client.get('/posts', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(len(data), 5)
        t.eq(data[4]['body'], 'HelloHelloHello')
        t.eq(rsp.headers['link'], '<http://localhost/posts?page=2>; rel="next"')

        rsp = self.client.get('/posts?page=2', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(len(data), 5)
        t.eq(data[0]['body'], 'HelloHelloHelloHello')
        t.eq(rsp.headers['link'], '<http://localhost/posts?page=1>; rel="prev", <http://localhost/posts?page=3>; rel="next"')

        rsp = self.client.get('/posts?page=3', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(rsp.headers['link'], '<http://localhost/posts?page=2>; rel="prev"')

        # Page doesn't exist
        rsp = self.client.get('/posts?page=4', headers=ajson)
        t.eq(rsp.status_code, 404)

        # Too much per page
        rsp = self.client.get('/posts?per_page=200', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(len(data), 5)

    def test_update(self):
        rsp = self.client.put('/posts/Hello', content_type='application/json',
                data='{"title":"Goodbye","body":"Goodbye World!"}')
        t.eq(rsp.status_code, 204)
        t.eq(mp.read_one({"title": "Goodbye"})['body'], "Goodbye World!")

    def test_delete(self):
        rsp = self.client.delete('/posts/Goodbye')
        t.eq(rsp.status_code, 204)
        t.eq(mp.read_many({"title": "Goodbye"}), [])
