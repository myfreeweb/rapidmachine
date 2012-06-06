# -*- coding: utf-8 -*-

import json
from math import ceil
from resource import Resource
from exceptions import FormattedHTTPException
from collections import defaultdict


def errors_to_dict(errors):
    """
    Turns a list of dictshield errors into a nice dict of errors,
    grouped by field.
    """
    # WTF, dictshield
    result = defaultdict(list)
    for error in errors:
        msg, field = str(error).split(':')[0].split(' - ')
        result[field].append(msg)
    return result


class DocumentResource(Resource):
    """
    A Resource with CRUD logic already implemented. You just have to set these
    attributes:
    * document = a dictshield.document.Document
    * persistence = a rapidmachine.persistence.Persistence
    * pk = a string -- the field of Document that's the primary key
      (used to construct URIs for redirection, eg. on POSTs)
    """

    # Class methods

    @classmethod
    def schema_resource(self):
        "Returns a resource which returns the JSON Schema of self.document"
        schema = self.document.to_jsonschema()

        class JSONSchemaResource(Resource):

            def content_types_provided(self, req, rsp):
                return [("application/json", self.to_json)]

            def to_json(self, req, rsp):
                return schema

        return JSONSchemaResource

    # Resource layer

    def __init__(self, req, rsp):
        self.links = {}

    def allowed_methods(self, req, rsp):
        """
        Decides whether the requested resource is the index or an entry,
        sets self.is_index accordingly and returns allowed methods
        """
        if len(req.matches) > 0:
            self.is_index = False
            return ["GET", "HEAD", "PUT", "DELETE"]
        else:
            self.is_index = True
            return ["GET", "HEAD", "POST"]

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
            self.raise_error(400, {"message": "Invalid JSON"})
        self.validate_and_process(data, req, rsp)

    def to_json(self, req, rsp):
        self.link_header(req, rsp)
        return json.dumps(self.data)

    def resource_exists(self, req, rsp):
        if req.method == "GET":
            if self.is_index:
                self.read_index(req, rsp)
            else:
                self.read_entry(req, rsp)
        # Not returning false, because we don't want html for 404s.
        # Raising exceptions instead.
        return True

    def post_is_create(self, req, rsp):
        return True

    def created_location(self, req, rsp):
        return req.url_object.add_path_segment(self.doc_instance[self.pk])

    def delete_resource(self, req, rsp):
        self.delete(req, rsp)
        return True

    # DocumentResource layer

    def default_per_page(self, req, rsp):
        return 20

    def max_per_page(self, req, rsp):
        return 100

    def raise_error(self, code, data):
        "Shorthand for raising FormattedHTTPException."
        self.data = data
        raise FormattedHTTPException(code)

    def validate_and_process(self, data, req, rsp):
        """
        Validates data parsed by from_*. If it's invalid, raises 422.
        If it's valid, creates or updates an instance in the database,
        whatever is appropriate for current request.
        """
        ex = self.document.validate_class_fields(data, validate_all=True)
        if len(ex) == 0:
            self.doc_instance = self.document(**data)
        else:
            self.raise_error(422, {
                "message": "Validation Failed",
                "errors": errors_to_dict(ex)
            })
        if self.is_index:
            self.create(req, rsp)
        else:
            self.update(req, rsp)

    def link_header(self, req, rsp):
        "Builds the Link header from self.links"
        rsp.headers['Link'] = ', '.join(['<%s>; rel="%s"' % (v, k)
            for (k, v) in self.links.iteritems()])

    def paginate(self, req, rsp):
        """
        Returns pagination data from current request:
        how many entries to skip, how many to show per page, the current page.
        """
        qs = req.url_object.query.dict
        per_page = int(qs['per_page']) if 'per_page' in qs \
                else self.default_per_page(req, rsp)
        if per_page > self.max_per_page(req, rsp):
            per_page = self.default_per_page(req, rsp)
        page = int(qs['page']) if 'page' in qs else 1
        skip = per_page * (page - 1)
        return (skip, per_page, page)

    def create(self, req, rsp):
        inst = self.doc_instance.to_python()
        self.persistence.create(inst)

    def read_index(self, req, rsp):
        # TODO: what if we need private fields? cut on to_json, etc.
        (skip, limit, page) = self.paginate(req, rsp)
        self.data = self.persistence.read_many(req.matches,
            fields=self.document._public_fields,
            skip=skip, limit=limit)
        # First page should return [] and not 404 if there's nothing
        if len(self.data) == 0 and page != 1:
            self.raise_error(404, {"message": "Page not found"})
        u = req.url_object
        pages = ceil(self.persistence.count() / float(limit))
        if page > 1:
            self.links['prev'] = u.set_query_param('page', str(page - 1))
        if page < pages:
            self.links['next'] = u.set_query_param('page', str(page + 1))

    def read_entry(self, req, rsp):
        self.data = self.persistence.read_one(req.matches,
                fields=self.document._public_fields)
        if not self.data:
            self.raise_error(404, {"message": "Document not found"})

    def update(self, req, rsp):
        inst = self.doc_instance.to_python()
        self.persistence.update(req.matches, inst)

    def delete(self, req, rsp):
        self.persistence.delete(req.matches)
