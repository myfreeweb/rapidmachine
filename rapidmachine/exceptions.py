# -*- coding: utf-8 -*-

import json
from werkzeug.exceptions import HTTPException


class FormatHTTPException(HTTPException):

    def __init__(self, code, ctype, dumps, dic):
        self.code = code
        self.ctype = ctype
        self.body = dumps(dic)
        super(FormatHTTPException, self).__init__()

    def get_headers(self, environ):
        return [('Content-Type', self.ctype)]

    def get_body(self, environ):
        return self.body


class JSONHTTPException(FormatHTTPException):

    def __init__(self, code, dic):
        super(JSONHTTPException, self).__init__(code, 'application/json',
                json.dumps, dic)
