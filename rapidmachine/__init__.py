# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))


def devserve(app, port=5000):  # pragma: no cover
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', port, app, use_debugger=True, use_reloader=True)

try:  # pragma: no cover
    from rapidmachine.resource import Resource
    from rapidmachine.documentresource import DocumentResource
    from rapidmachine.app import App, Var, Route
    __all__ = ["devserve", "__version__", "App", "Resource",
            "DocumentResource", "Var", "Route"]
except ImportError:  # pragma: no cover
    import traceback
    traceback.print_exc()
