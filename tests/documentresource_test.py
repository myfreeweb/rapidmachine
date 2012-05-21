import t
import json
from werkzeug.test import Client
from werkzeug.wrappers import Response
from rapidmachine import App, R, V, DocumentResource
from rapidmachine.persistence import MemoryPersistence
from dictshield.document import Document
from dictshield.fields import StringField


ajson = {'Accept': 'application/json'}
mp = MemoryPersistence()


class Post(Document):
    _public_fields = ['title', 'body']
    title = StringField(max_length=64)
    body  = StringField(max_length=1024)


class PostResource(DocumentResource):
    document    = Post
    persistence = mp
    pk          = 'title'
    default_per_page = 5


class TestApp(App):
    handlers = [
        R(['posts'], PostResource),
        R(['posts', V('title', str)], PostResource),
        R(['posts.schema'], PostResource.schema_resource()),
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

    def test_read_index(self):
        rsp = self.client.get('/posts', headers=ajson)
        t.eq(rsp.status_code, 200)
        t.eq(json.loads(rsp.data), [{"title": "Hello", "body": "Hello World!"}])

    def test_read_invalid(self):
        rsp = self.client.get('/posts/Goodbye', headers=ajson)
        t.eq(rsp.status_code, 404)

    def test_read_schema(self):
        rsp = self.client.get('/posts.schema', headers=ajson)
        t.eq(json.loads(rsp.data)['type'], 'object')
        t.eq(rsp.status_code, 200)

    def test_read_paginated(self):
        for n in range(0, 100):
            mp.create({'title': 'yo', 'body': 'Hello' * n})
        rsp = self.client.get('/posts', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(len(data), 5)
        t.eq(data[4]['body'], 'HelloHelloHello')
        rsp = self.client.get('/posts?page=2', headers=ajson)
        data = json.loads(rsp.data)
        t.eq(len(data), 5)
        t.eq(data[0]['body'], 'HelloHelloHelloHello')
