Tutorial
========

Your first app
--------------

Create a file called `app.py` with this code::

    from rapidmachine import App, R, V, Resource, devserve

    class HelloResource(Resource):
        def to_html(self, req, rsp):
            return "Hello " + req.matches["username"]

    class HelloApp(App):
        handlers = [
            R(["hello", V("username")], HelloResource)
        ]

    if __name__ == "__main__":
        devserve(HelloApp())

Run it and try making a request::

    $ python app.py
    $ curl localhost:5000/hello/world
    Hello world
