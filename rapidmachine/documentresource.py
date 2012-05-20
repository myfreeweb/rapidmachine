# -*- coding: utf-8 -*-

import json
from resource import Resource
from exceptions import JSONHTTPException
from collections import defaultdict


def errors_to_dict(errors):
    # WTF, dictshield
    result = defaultdict(list)
    for error in errors:
        msg, field = str(error).split(':')[0].split(' - ')
        result[field].append(msg)
    return result


class DocumentResource(Resource):

    def __init__(self, req, rsp):
        self.data = {}

    def allowed_methods(self, req, rsp):
        return ["GET", "HEAD", "POST", "PUT", "DELETE"]

    def content_types_accepted(self, req, rsp):
        return [
            ("application/json", self.from_json)
        ]

    def content_types_provided(self, req, rsp):
        return [
            ("application/json", self.to_json)
        ]

    def from_json(self, req, rsp):
        try:
            data = json.loads(req.data)
        except ValueError:
            raise JSONHTTPException(400, {"error": "Invalid JSON"})
        ex = self.document.validate_class_fields(data, validate_all=True)
        if len(ex) == 0:
            self.documentize(data)
        else:
            raise JSONHTTPException(400, errors_to_dict(ex))

    def to_json(self, req, rsp):
        return self.document.make_json_publicsafe(self.doc_instance)

    def resource_exists(self, req, rsp):
        if len(req.matches) == 0:  # read index / create
            return True
        else:  # read/update/delete entry
            data = self.persistence.read_one(req.matches)
            if data:
                self.documentize(data)
            return bool(data)

    def documentize(self, data):
        self.doc_instance = self.document(**data)

    def post_is_create(self, req, rsp):
        return True

    def created_location(self, req, rsp):
        inst = self.doc_instance.to_python()
        self.persistence.create(inst)
        return req.url_object.add_path_segment(inst[self.pk])
