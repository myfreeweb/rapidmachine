# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))

def devserve(app, port=5000):
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', port, app, use_debugger=True, use_reloader=True)

try:
    from rapidmachine.resource import Resource
except ImportError:
    import traceback
    traceback.print_exc()
