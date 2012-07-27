Tutorial
========

.. module:: rapidmachine

Your first app
--------------

Create a file called `app.py` with this code::

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

Run it and try making a request::

    $ python app.py
    $ curl localhost:5000/hello/world
    Hello world

In this example, you created a resource and an app.

An app (instance of :class:`App`) is a WSGI application that routes requests to Resources.
When it's called by a WSGI server, it creates a request object and a response object (by default, :class:`werkzeug.wrappers.Request` and :class:`werkzeug.wrappers.Response`, but you can override request_class and response_class to use subclasses of these).
Then it finds a matching handler (Resource) and passes all three to the decision core.
It also adds two attributes to the Request object:

* url_object -- a `URLObject`_ for the requested URL
* matches -- a dictionary of matched variables

A resource (subclass of :class:`Resource`) is a class with methods which answer questions (e.g. does this resource exist?) and do things (e.g. delete it).

Routing
-------

Routes are stored in the `handlers` attribute of your app.
A route is a dictionary with `route` set to a list of URL parts and `res` to the resource.
You shouldn't create dictionaries manually.
Use the :class:`Route` shorthand instead.

URL parts are strings and variables (instances of :class:`Var`).
Variables can have types.

For example, this matches `/posts` and `/posts/123` but not `/posts/hello`::

    handlers = [
        Route("posts").to(PostResource)
        Route("posts", Var("id", int)).to(PostResource)
    ]

And in your resource's methods, `req.matches["id"]` will be `123` (an int) if you request `/posts/123`.

Writing Resources
-----------------

As I've already mentioned, Resources are classes that answer questions about the request.
You can look at the documentation of the class :class:`Resource` to see the list of methods you can override.
Even though you should use DocumentResource to make CRUD (Create-Read-Update-Delete) endpoints, let's create one manually to understand how that works::

    import json
    from rapidmachine import App, Route, Var, Resource
    from rapidmachine.persistence import MemoryPersistence

    class CRUDResource(Resource):
        persistence = MemoryPersistence()
        pk = "title"

        def allowed_methods(self, req, rsp):
            # here we decide whether the index or a record is requested, store it and return, well, allowed methods
            # on /records, req.matches == {}
            # on /records/something, req.matches == {"title": "something"}
            # the key "title" comes from the name of the Var in routes
            if len(req.matches) > 0:
                self.is_index = False
                return ["GET", "HEAD", "PUT", "DELETE"]
            else:
                self.is_index = True
                return ["GET", "HEAD", "POST"]

        def content_types_accepted(self, req, rsp):
            return [ ("application/json", self.from_json) ]

        def content_types_provided(self, req, rsp):
            return [ ("application/json", self.to_json) ]

        def from_json(self, req, rsp):
            self.data = json.loads(req.data)
            # note: create/update depends on whether it's the index or a record,
            # not POST or PUT. so you can allow POST on records to update if you want
            if self.is_index:
                self.persistence.create(self.data)
            else:
                self.persistence.update(req.matches, self.data)

        def to_json(self, req, rsp):
            return json.dumps(self.data)

        def resource_exists(self, req, rsp):
            # this both performs reading and makes sure the resource exists
            if self.is_index:
                if req.method != "POST":
                    self.data = self.persistence.read_many(req.matches)
            else:
                self.data = self.persistence.read_one(req.matches)
                if not self.data:
                    return False
            return True

        def post_is_create(self, req, rsp):
            return True

        def created_location(self, req, rsp):
            return req.url_object.add_path_segment(self.data[self.pk]).path

        def delete_resource(self, req, rsp):
            self.persistence.delete(req.matches)
            return True

    class CRUDApp(App):
        handlers = [
            Route("records").to(CRUDResource),
            Route("records", Var("title")).to(CRUDResource)
        ]

    if __name__ == "__main__":
        CRUDApp().devserve()

This is much more basic than :class:`DocumentResource` -- there's no pagination, no validation, no hypermedia.
But this shows how it works.
The `pk` property is only used in `created_location` to build URLs.
The name of the Var in the second route (which is the same!) builds the query.

Using and customizing DocumentResource
--------------------------------------

Now, the most interesting part!
The reason why RapidMachine was created!
Not typing things like `self.persistence.create(self.data)` every time you make a resource.

Let's make a DocumentResource subclass that will add the date and time of creation automatically and won't let the user override it::

    from datetime import datetime
    from rapidmachine import App, Route, Var, DocumentResource
    from rapidmachine.persistence import MemoryPersistence
    from dictshield.document import Document
    from dictshield.fields import StringField, DateTimeField

    class Post(Document):
        _public_fields = ["title", "body", "created_at"]
        title = StringField(max_length=64)
        body = StringField(max_length=1024)
        created_at = DateTimeField()

    class PostResource(DocumentResource):
        document    = Post
        persistence = MemoryPersistence()
        pk          = "title"

        def create(self, req, rsp, data):
            data["created_at"] = datetime.now()
            super(PostResource, self).create(req, rsp, data)

        def update(self, req, rsp, data):
            del data["created_at"]
            super(PostResource, self).update(req, rsp, data)

    class PostsApp(App):
        handlers = [
            Route("posts").to(PostResource),
            Route("posts", Var("title")).to(PostResource)
        ]

    if __name__ == "__main__":
        PostsApp().devserve()

Now we can create a post and try to update created_at::

    $ curl -XPOST -d '{"title": "Hello", "body": "world"}' -H 'Content-Type: application/json' localhost:5000/posts
    $ curl localhost:5000/posts
    [{"body": "world", "created_at": "2012-07-27T22:00:00.580299", "title": "Hello"}]
    $ curl -XPUT -d '{"title": "Hello", "body": "world", "2011-01-21T11:11:11"}' -H 'Content-Type: application/json' localhost:5000/posts/Hello
    $ curl localhost:5000/posts
    [{"body": "world", "created_at": "2012-07-27T22:00:00.580299", "title": "Hello"}]

Now delete the `update` override and try doing the same -- you can store the new date.

.. _URLObject: https://github.com/zacharyvoase/urlobject
