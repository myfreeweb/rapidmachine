# RapidMachine [![Build Status](https://secure.travis-ci.org/myfreeweb/rapidmachine.png)](http://travis-ci.org/myfreeweb/rapidmachine)

RAD + API = RAPID.  
Rapid Application Development + Application Programming Interface = Rapid Application Programming Interface Development.

RapidMachine is a RAPID toolkit for Python, based on a [Webmachine](http://wiki.basho.com/Webmachine.html)-style HTTP abstraction and built on [Werkzeug](http://werkzeug.pocoo.org).

## Get excited

Zero-boilerplate CRUD for a [dictshield](https://github.com/j2labs/dictshield) model and MongoDB:

```python
import pymongo
from rapidmachine import App, Route, Var, DocumentResource
from rapidmachine.persistence import MongoPersistence
from dictshield.document import Document
from dictshield.fields import StringField

db = pymongo.Connection().database

class Post(Document):
    _public_fields = ['title', 'body']
    title = StringField(max_length=64)
    body  = StringField(max_length=1024)

class PostResource(DocumentResource):
    document    = Post
    persistence = MongoPersistence(db, 'posts')
    pk          = 'title'

class PostsApp(App):
    handlers = [
        Route("posts").to(PostResource),
        Route("posts", Var("title")).to(PostResource)
    ]

if __name__ == "__main__":
    PostsApp().devserve()
```

## [Docs](http://rapidmachine.rtfd.org/)
