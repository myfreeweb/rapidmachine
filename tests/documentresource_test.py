import t
from should_dsl import *
try:
    import json
except ImportError: # Python 2.5
    import simplejson as json
from rapidmachine import (
    App, Route, Var,
    DocumentResource, EmbeddedDocumentResource
)
from rapidmachine.persistence import MemoryPersistence
from dictshield.document import Document, EmbeddedDocument
from dictshield.fields import StringField
from dictshield.fields.compound import ListField, EmbeddedDocumentField


ajson = {"Accept": "application/json"}
hjson = {"Accept": "application/hal+json"}
mp = MemoryPersistence()


class Comment(EmbeddedDocument):
    _public_fields = ["body", "uid"]
    body  = StringField(max_length=1024)
    uid   = StringField(max_length=32)


class Post(Document):
    _public_fields = ["title", "body"]
    title    = StringField(max_length=64)
    body     = StringField(max_length=1024)
    comments = ListField(EmbeddedDocumentField(Comment))


class PostResource(DocumentResource):
    document    = Post
    persistence = mp
    pk          = "title"

    def default_per_page(self, req, rsp):
        return 5


class CommentResource(EmbeddedDocumentResource):
    document  = Comment
    pk        = "uid"
    field     = "comments"
    parent_pk = "title"
    parent_persistence = mp


class TestApp(App):
    handlers = [
        Route("posts").to(PostResource),
        Route("posts", Var("title")).to(PostResource),
        Route("posts", Var("__title"), "comments").to(CommentResource),
        Route("posts", Var("__title"), "comments", Var("uid")).to(CommentResource),
        Route("posts.schema").to(PostResource.schema_resource()),
    ]


class AppTest(t.Test):

    def setUp(self):
        self.client = TestApp().test_client()

    def test_create_valid(self):
        rsp = self.client.post("/posts", content_type="application/json",
                data='{"title":"Hello","body":"Hello World!"}')
        rsp.headers["location"] |should_be.equal_to| "http://localhost/posts/Hello"

        rsp = self.client.post("/posts/Hello/comments", content_type="application/json",
                data='{"uid":"abc","body":"Hello World!"}')
        rsp.headers["location"] |should_be.equal_to| "http://localhost/posts/Hello/comments/abc"

    def test_create_invalid_format(self):
        rsp = self.client.post("/posts", content_type="application/json",
                data='{"title":Hello""body":"Hello!"')
        rsp.status_code |should_be.equal_to| 400

    def test_create_invalid_data(self):
        rsp = self.client.post("/posts", content_type="application/json",
                data='{"title":"%s","body":"Hello World!"}' % ("Hello" * 128))
        rsp.status_code |should_be.equal_to| 422
        json.loads(rsp.data)["errors"] |should_be.equal_to| {"title": ["String value is too long"]}

    def test_read_valid(self):
        rsp = self.client.get("/posts/Hello", headers=ajson)
        rsp.status_code |should_be.equal_to| 200
        json.loads(rsp.data) |should_be.equal_to| {"title": "Hello", "body": "Hello World!"}

        rsp = self.client.get("/posts/Hello", headers=hjson)
        json.loads(rsp.data) |should_be.equal_to| {
            "_links": {"self": {"href": "/posts/Hello"},
                       "comments": {"href": "/posts/Hello/comments"}},
            "title": "Hello",
            "body": "Hello World!"
        }

        rsp = self.client.get("/posts/Hello/comments/abc", headers=ajson)
        rsp.status_code |should_be.equal_to| 200
        json.loads(rsp.data) |should_be.equal_to| {"uid": "abc", "body": "Hello World!"}

    def test_read_index(self):
        rsp = self.client.get("/posts", headers=ajson)
        rsp.status_code |should_be.equal_to| 200
        json.loads(rsp.data) |should_be.equal_to| [{"title": "Hello", "body": "Hello World!"}]

        rsp = self.client.get("/posts", headers=hjson)
        json.loads(rsp.data) |should_be.equal_to| {
            "_links": {"self": {"href": "/posts"}},
            "_embedded": {
                "post": [
                    {
                        "_links": {"self": {"href": "/posts/Hello"},
                                   "comments": {"href": "/posts/Hello/comments"}},
                        "title": "Hello",
                        "body": "Hello World!"
                    }
                ]
            }
        }

        rsp = self.client.get("/posts/Hello/comments", headers=ajson)
        rsp.status_code |should_be.equal_to| 200
        json.loads(rsp.data) |should_be.equal_to| [{"uid": "abc", "body": "Hello World!"}]

    def test_read_invalid(self):
        rsp = self.client.get("/posts/Goodbye", headers=ajson)
        rsp.status_code |should_be.equal_to| 404

        rsp = self.client.get("/posts/Hello/comments/cba", headers=ajson)
        rsp.status_code |should_be.equal_to| 404

    def test_read_schema(self):
        rsp = self.client.get("/posts.schema", headers=ajson)
        json.loads(rsp.data)["type"] |should_be.equal_to| "object"
        rsp.status_code |should_be.equal_to| 200

    def test_read_paginated(self):
        for n in range(0, 11):
            mp.create({"title": "yo", "body": "Hello" * n})

        # Happy cases
        rsp = self.client.get("/posts", headers=ajson)
        data = json.loads(rsp.data)
        len(data) |should_be.equal_to| 5
        data[4]["body"] |should_be.equal_to| "HelloHelloHello"
        rsp.headers["link"] |should_be.equal_to| '<http://localhost/posts?page=2>; rel="next"'

        rsp = self.client.get("/posts?page=2", headers=ajson)
        data = json.loads(rsp.data)
        len(data) |should_be.equal_to| 5
        data[0]["body"] |should_be.equal_to| "HelloHelloHelloHello"
        rsp.headers["link"] |should_be.equal_to| '<http://localhost/posts?page=1>; rel="prev", <http://localhost/posts?page=3>; rel="next"'

        rsp = self.client.get("/posts?page=3", headers=ajson)
        data = json.loads(rsp.data)
        rsp.headers["link"] |should_be.equal_to| '<http://localhost/posts?page=2>; rel="prev"'

        # Page doesn"t exist
        rsp = self.client.get("/posts?page=4", headers=ajson)
        rsp.status_code |should_be.equal_to| 404

        # Too much per page
        rsp = self.client.get("/posts?per_page=200", headers=ajson)
        data = json.loads(rsp.data)
        len(data) |should_be.equal_to| 5

    def test_update(self):
        rsp = self.client.put("/posts/Hello", content_type="application/json",
                data='{"title":"Goodbye","body":"Goodbye World!"}')
        rsp.status_code |should_be.equal_to| 204
        mp.read_one({"title": "Goodbye"})["body"] |should_be.equal_to| "Goodbye World!"
        len(mp.read_one({"title": "Goodbye"})["comments"]) |should_be.equal_to| 1

        rsp = self.client.put("/posts/Nothing", content_type="application/json",
                data='{"some": "thing"}')
        rsp.status_code |should_be.equal_to| 404

        rsp = self.client.put("/posts/Goodbye/comments/abc", content_type="application/json",
                data='{"uid":"abc","body":"Goodbye World!"}')
        rsp.status_code |should_be.equal_to| 204
        mp.read_one({"title": "Goodbye"})["comments"][0]["body"] |should_be.equal_to| "Goodbye World!"

    def test_delete(self):
        mp.create({"title": "Goodbye", "comments": [{"uid": "abc", "body":
            "Hello World!"}], "body": "Hello World!"})
        rsp = self.client.delete("/posts/Goodbye/comments/abc")
        rsp.status_code |should_be.equal_to| 204
        mp.read_one({"title": "Goodbye"})["comments"] |should_be.equal_to| []

        rsp = self.client.delete("/posts/Goodbye")
        rsp.status_code |should_be.equal_to| 204
        mp.read_many({"title": "Goodbye"}) |should_be.equal_to| []

        rsp = self.client.delete("/posts/Nothing")
        rsp.status_code |should_be.equal_to| 404
