RapidMachine
============

RapidMachine is a Rapid API Development toolkit for Python.
It's based on a `Webmachine`_-style HTTP abstraction and built on `Werkzeug`_.
The simplest app looks like this::

    from rapidmachine import App, Route, Var, Resource

    class HelloResource(Resource):
        def to_html(self, req, rsp):
            return "Hello " + req.matches["username"]

    class HelloApp(App):
        handlers = [
            Route("hello", Var("username")).to(HelloResource)
        ]

    if __name__ == "__main__":
        HelloApp().devserve()

But there's much more to RapidMachine.
For example, zero-boilerplate CRUD::

    import pymongo
    from rapidmachine import App, Route, Var, DocumentResource
    from rapidmachine.persistence import MongoPersistence
    from dictshield.document import Document
    from dictshield.fields import StringField

    db = pymongo.Connection().database

    class Post(Document):
        _public_fields = ["title", "body"]
        title = StringField(max_length=64)
        body  = StringField(max_length=1024)

    class PostResource(DocumentResource):
        document    = Post
        persistence = MongoPersistence(db, "posts")
        pk          = "title"

    class PostsApp(App):
        handlers = [
            Route("posts").to(PostResource),
            Route("posts", Var("title")).to(PostResource)
        ]

    if __name__ == "__main__":
        PostsApp().devserve()

This example shows all you need to make a CRUD endpoint for a dictshield model connected to MongoDB.
POST to localhost:5000/posts to make an entry, GET it to get a list of entries, PUT and DELETE localhost:5000/posts/title to do... you guessed it, updating and deletion.

Documentation
-------------

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   reference

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`

.. _Webmachine: http://wiki.basho.com/Webmachine.html
.. _Werkzeug: http://werkzeug.pocoo.org
