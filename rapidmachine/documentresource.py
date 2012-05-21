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
        if not hasattr(self, 'default_per_page'):
            self.default_per_page = 20
        if not hasattr(self, 'max_per_page'):
            self.max_per_page = 100

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
            raise JSONHTTPException(400, {"message": "Invalid JSON"})
        ex = self.document.validate_class_fields(data, validate_all=True)
        if len(ex) == 0:
            self.doc_instance = self.document(**data)
        else:
            raise JSONHTTPException(422, {
                "message": "Validation Failed",
                "errors": errors_to_dict(ex)
            })

    def to_json(self, req, rsp):
        return json.dumps(self.data)

    def paginate(self, req, rsp):
        qs = req.url_object.query.dict
        per_page = int(qs['per_page']) if 'per_page' in qs else self.default_per_page
        if per_page > self.max_per_page:
            per_page = self.default_per_page
        page = int(qs['page']) if 'page' in qs else 1
        skip = per_page * (page - 1)
        return (skip, per_page, page)

    def resource_exists(self, req, rsp):
        # Not using dictshield to cut private fields,
        # because the database can filter.
        if len(req.matches) == 0:  # read index / create
            if req.method == "GET":
                (skip, limit, page) = self.paginate(req, rsp)
                self.data = self.persistence.read_many(req.matches,
                    fields=self.document._public_fields,
                    skip=skip, limit=limit)
                if len(self.data) == 0 and page != 1:
                    raise JSONHTTPException(404, {"message": "Page not found"})
        else:  # read/update/delete entry
            self.data = self.persistence.read_one(req.matches,
                    fields=self.document._public_fields)
            if not self.data:
                raise JSONHTTPException(404, {"message": "Document not found"})
        # Not returning false, because we don't want html for 404s.
        # Raising exceptions instead.
        return True

    def post_is_create(self, req, rsp):
        return True

    def created_location(self, req, rsp):
        inst = self.doc_instance.to_python()
        self.persistence.create(inst)
        return req.url_object.add_path_segment(inst[self.pk])

    @classmethod
    def schema_resource(self):
        schema = self.document.to_jsonschema()

        class JSONSchemaResource(Resource):

            def content_types_provided(self, req, rsp):
                return [("application/json", self.to_json)]

            def to_json(self, req, rsp):
                return schema

        return JSONSchemaResource
