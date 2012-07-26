# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))


try:  # pragma: no cover
    from rapidmachine.resource import Resource
    from rapidmachine.documentresource import DocumentResource, \
            EmbeddedDocumentResource
    from rapidmachine.app import App, Var, Route
    __all__ = ["__version__", "App", "Resource",
               "DocumentResource", "EmbeddedDocumentResource",
               "Var", "Route"]
except ImportError:  # pragma: no cover
    import traceback
    traceback.print_exc()
