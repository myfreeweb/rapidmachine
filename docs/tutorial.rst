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

How that works
--------------

In this example, you created a resource and an app.

An app (instance of :class:`App`) is a WSGI application that routes requests to Resources.
When it's called by a WSGI server, it creates a request object (:class:`werkzeug.wrappers.Request`) and a response object (:class:`werkzeug.wrappers.Response`).
Then it finds a matching handler and passes all three to the decision core
It also adds two attributes to the Request object:

* url_object -- `URLObject`_ for the requested URL
* matches -- a dictionary of matched variables

A resource (instance of :class:`Resource`) is an object with methods which answer questions (e.g. does this resource exist?) and do things (e.g. delete it).

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

.. _URLObject: https://github.com/zacharyvoase/urlobject
