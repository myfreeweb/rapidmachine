# -*- coding: utf-8 -*-


class FormattedHTTPException(Exception):

    def __init__(self, code):
        self.code = code
        super(Exception, self).__init__()


class InvalidAuthException(Exception):

    def __init__(self):
        super(Exception, self).__init__()
