# [RapidMachine](https://github.com/myfreeweb/rapidmachine)
# is a Rapid API Development toolkit for Python.
# For now, it includes a Webmachine-style HTTP abstraction.

# Let's make a simple web service now.
# Start with imports.
from rapidmachine import App, R, V, Resource, devserve

# Now, let's make our first resource.
# A resource is just a collection of functions that are called by RapidMachine's
# decision core. They take the current request and response
# ([Werkzeug objects](http://werkzeug.pocoo.org/docs/wrappers/)) and answer
# simple questions like "does this exist?", "which methods are allowed?",
# "is this forbidden?", do what's requested (get, post, put, delete) and convert
# the response to various content types.
class TestRes(Resource):
    def to_html(self, req, rsp):
        return "Hi, %s" % req.matches['username']

# And an app.
# Apps (instances of App or your subclass) are WSGI applications that
# route requests to Resources.
# The syntax for routes is pretty simple. We don't have nice symbols/atoms in
# Python, but we can make variables typed!
class TestApp(App):
    handlers = [
        R(['hello', V('username', str)], TestRes)
    ]

# We can use devserve to start a development server.
if __name__ == '__main__':
    devserve(App())

# Now, we can do something like  
# $ curl localhost:5000/hello/myfreeweb  
# and we'll get "Hi, myfreeweb"
