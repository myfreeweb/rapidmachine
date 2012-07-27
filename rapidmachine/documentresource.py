# -*- coding: utf-8 -*-

try:
    import json
except ImportError:  # pragma: no cover
    import simplejson as json
from math import ceil
from resource import Resource
from exceptions import FormattedHTTPException
from persistence import EmbeddedPersistence
from collections import defaultdict
from dictshield.fields.compound import ListField


def errors_to_dict(errors):
    """
    Turns a list of dictshield errors into a nice dict of errors,
    grouped by field.
    """
    # WTF, dictshield
    result = defaultdict(list)
    for error in errors:
        msg, field = str(error).split(":")[0].split(" - ")
        result[field].append(msg)
    return result


class DocumentResource(Resource):
    """
    A Resource with CRUD logic already implemented.

    This class is meant to be subclassed. You just have to set these
    attributes:

    * document = a `dictshield`_.document.Document
    * persistence = a :class:`rapidmachine.persistence.Persistence`
    * pk = a string -- the field of Document that's the primary key
      (used to construct URIs for redirection, eg. on POSTs)
    * store_types = a boolean (default is False) -- whether to store
      dictshield's metadata (_types, _cls) -- set to True if you have
      subclasses stored in one collection

    .. _dictshield: https://github.com/j2labs/dictshield
    """

    # Properties

    store_types = False

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
        self.is_error = False
        self.links = {}
        self.listfields = []
        for k, v in self.document._fields.iteritems():
            if isinstance(v, ListField):
                self.listfields.append(k)

    def allowed_methods(self, req, rsp):
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
            ("application/json", self.to_json),
            ("application/vnd.hal+json", self.to_hal_json),
            ("application/hal+json", self.to_hal_json)
        ]

    def from_json(self, req, rsp):
        try:
            data = json.loads(req.data)
        except ValueError:
            self.raise_error(400, {"message": "Invalid JSON"})
        self.validate_and_process(req, rsp, data)

    def to_json(self, req, rsp):
        self.link_header(req, rsp)
        if self.is_error:
            return json.dumps(self.data)
        else:
            if self.is_index:
                return json.dumps([
                    self._process_data(
                        self._get_doc_instance(d).to_json(encode=False),
                        delete_listfields=True
                    ) for d in self.data])
            else:
                return json.dumps(self._process_data(
                        self._get_doc_instance(self.data).to_json(encode=False),
                        delete_listfields=True))

    def to_hal_json(self, req, rsp):
        def hrefify(iterator):
            return dict([(k, {"href": v}) for k, v in iterator])
        links = hrefify(self.links.iteritems())
        links["self"] = {"href": req.url_object.path}
        data = self.data
        if self.is_index:
            for inst in data:
                inst["_links"] = hrefify(self.inst_links(req, rsp,
                    inst).iteritems())
            return json.dumps({
                "_links": links,
                "_embedded": {self.hal_type(req, rsp): data}
            })
        else:
            data["_links"] = links
        return json.dumps(data)

    def resource_exists(self, req, rsp):
        if self.is_index:
            if req.method != "POST":
                self.read_index(req, rsp)
        else:
            self.read_entry(req, rsp)
        # Not returning false, because we don't want html for 404s.
        # Raising exceptions instead.
        return True

    def post_is_create(self, req, rsp):
        return True

    def created_location(self, req, rsp):
        return self.inst_self_link(req, rsp, self.doc_instance).path

    def delete_resource(self, req, rsp):
        self.delete(req, rsp)
        return True

    # DocumentResource layer

    def inst_self_link(self, req, rsp, inst):
        if self.is_index:
            return req.url_object.add_path_segment(inst[self.pk])
        else:
            return req.url_object

    def inst_links(self, req, rsp, inst):
        sl = self.inst_self_link(req, rsp, inst)
        links = {"self": sl.path}
        for k in self.listfields:
                links[k] = sl.add_path_segment(k).path
        return links

    def hal_type(self, req, rsp):
        """
        Return the type for HAL format, by default the classname without
        'Resource', all lowercased."""
        return self.__class__.__name__.replace("Resource", "").lower()

    def default_per_page(self, req, rsp):  # pragma: no cover
        "Returns the default number of entries per page. By default, 20."
        return 20

    def max_per_page(self, req, rsp):  # pragma: no cover
        "Returns the maximum number of entries per page. By default, 100."
        return 100

    def raise_error(self, code, data):
        self.data = data
        self.is_error = True
        raise FormattedHTTPException(code)

    def validate_and_process(self, req, rsp, data):
        """
        Validates data parsed by from_*. If it's invalid, raises 422.
        If it's valid, creates or updates an instance in the database,
        whatever is appropriate for current request.
        """
        # screw you, dictshield
        # y u no parse dates and stuff on .validate_class_fields?!
        try:
            data = self._process_data(self._get_doc_instance(data).to_python())
        except:
            pass
        ex = self.document.validate_class_fields(data, validate_all=True)
        if len(ex) == 0:
            self.doc_instance = self._get_doc_instance(data)
        else:
            self.raise_error(422, {
                "message": "Validation Failed",
                "errors": errors_to_dict(ex)
            })
        data = self._process_data(self.doc_instance.to_python())
        if self.is_index:
            self.create(req, rsp, data)
        else:
            self.update(req, rsp, data)

    def _process_data(self, data, delete_listfields=False):
        if not self.store_types:
            if "_types" in data:
                del data["_types"]
            if "_cls" in data:
                del data["_cls"]
        if delete_listfields:
            for k in self.listfields:
                if k in data:
                    del data[k]
        return data

    def _get_doc_instance(self, data):
        try:
            doc_instance = self.document(**data)
        except TypeError:  # pragma: no cover
            # On Python 2.5, you can't use a dict with unicode keys
            data_converted = dict([(str(k), v) for k, v in data.items()])
            doc_instance = self.document(**data_converted)
        return doc_instance

    def link_header(self, req, rsp):
        """
        Builds the Link header from self.links. Invoke this from to_*
        methods for formats that don't contain links.
        """
        rsp.headers["Link"] = ", ".join(['<%s>; rel="%s"' % (v, k)
            for k, v in self.links.iteritems()])

    def paginate(self, req, rsp):
        """
        Returns pagination data from current request:
        how many entries to skip, how many to show per page, the current page.
        """
        qs = req.url_object.query.dict
        per_page = int(qs["per_page"]) if "per_page" in qs \
                else self.default_per_page(req, rsp)
        if per_page > self.max_per_page(req, rsp):
            per_page = self.default_per_page(req, rsp)
        page = int(qs["page"]) if "page" in qs else 1
        skip = per_page * (page - 1)
        return (skip, per_page, page)

    def create(self, req, rsp, data):
        "Creates a new object in the database."
        self.persistence.create(data)

    def read_index(self, req, rsp):
        """
        Retrieves a list of instances from the database for the requested page,
        sets self.data and self.links appropriately.
        Raises 404 if the requested page doesn't exist (i.e. there aren't
        enough instances).
        """
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
            self.links["prev"] = u.set_query_param("page", str(page - 1))
        if page < pages:
            self.links["next"] = u.set_query_param("page", str(page + 1))

    def read_entry(self, req, rsp):
        """
        Retrieves a matching instance from the database and sets
        self.data to it.
        Raises 404 if there isn't a matching instance.
        """
        self.data = self.persistence.read_one(req.matches,
                fields=self.document._public_fields)
        if not self.data:
            self.raise_error(404, {"message": "Document not found"})
        self.links = self.inst_links(req, rsp, self.data)

    def update(self, req, rsp, data):
        "Updates a matching object in the database."
        data = self._process_data(data, delete_listfields=True)
        self.persistence.update(req.matches, data)

    def delete(self, req, rsp):
        "Deletes a matching object in the database."
        self.persistence.delete(req.matches)

class EmbeddedDocumentResource(DocumentResource):
    """
    A DocumentResource for embedded lists of resources.

    This class is meant to be subclassed. You just have to set these
    attributes:

    * document = a `dictshield`_.document.Document
    * parent_persistence = a :class:`rapidmachine.persistence.Persistence`
    * parent_pk = a string -- the field of the parent document that's the primary key
    * pk = a string -- the field of the embedded document that's the primary key
    * field = a string -- which field of the parent document is a ListField
      that's a list of embedded documents
    * store_types = a boolean (default is False) -- whether to store
      dictshield's metadata (_types, _cls) -- set to True if you have
      subclasses stored in one collection

    .. _dictshield: https://github.com/j2labs/dictshield
    """


    def __init__(self, req, rsp):
        DocumentResource.__init__(self, req, rsp)
        parent_matches = {}
        for k, v in list(req.matches.iteritems()):
            if k[:2] == "__":
                parent_matches[k[2:]] = v
                del req.matches[k]
        self.persistence = EmbeddedPersistence(self.parent_persistence,
                parent_matches, self.field)
