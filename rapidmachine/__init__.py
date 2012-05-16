# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
__version__ = ".".join(map(str, version_info))

try:
    from rapidmachine.decisions import process
    from rapidmachine.resource import Resource
except ImportError:
    import traceback
    traceback.print_exc()
