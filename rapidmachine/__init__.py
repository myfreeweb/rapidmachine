# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))


def devserve(app, port=5000):
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', port, app, use_debugger=True, use_reloader=True)

try:
    from rapidmachine.resource import Resource
    from rapidmachine.documentresource import DocumentResource
    from rapidmachine.app import App, V, R
    __all__ = ["devserve", "__version__", "App", "Resource",
            "DocumentResource", "V", "R"]
except ImportError:
    import traceback
    traceback.print_exc()
