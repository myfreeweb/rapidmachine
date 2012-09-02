# -*- coding: utf-8 -*-
from __future__ import absolute_import
try:
    import json
except ImportError:  # pragma: no cover
    import simplejson as json
from ..resource import Resource
from ..exceptions import FormattedHTTPException

class AccountResource(Resource):
    """
    The singleton resource used for registration,
    viewing, editing and deleting user's account.
    """

    def allowed_methods(self, req, rsp):
        return ["GET", "HEAD", "POST", "PUT", "DELETE"]

    def post_is_create(self, req, rsp):
        return True

    def resource_exists(self, req, rsp):
        self.data = req.user
        return True

    def created_location(self, req, rsp):
        return req.url_object.path

    def content_types_accepted(self, req, rsp):
        return [ ("application/json", self.from_json) ]

    def content_types_provided(self, req, rsp):
        return [ ("application/json", self.to_json) ]

    def raise_error(self, code, data):
        self.data = data
        self.is_error = True
        raise FormattedHTTPException(code)

    def to_json(self, req, rsp):
        return json.dumps(self.data)

    def from_json(self, req, rsp):
        try:
            data = json.loads(req.data)
        except ValueError:
            self.raise_error(400, {"message": "Invalid JSON"})
        if req.method == "POST":
            if not self.backend.username_field in data:
                self.raise_error(400, {"message": "No username"})
            if not self.backend.password_field in data:
                self.raise_error(400, {"message": "No password"})
            r = self.backend.create_user(
                    data[self.backend.username_field],
                    data[self.backend.password_field],
                    data)
            if r == False:
                self.raise_error(400, {"message":
                    "A user with this name already exists"})
        else:
            self.backend.update_user(req.user, data)

    def delete_resource(self, req, rsp):
        self.backend.delete_user(req.user)
        return True
