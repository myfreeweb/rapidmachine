# -*- coding: utf-8 -*-


class Resource(object):
    """
    An object that contains logic for one or more
    HTTP endpoints. The logic is contained in methods that accept
    (self, req, rsp), where req is an instance of
    :class:`werkzeug.wrappers.Request` and rsp is an instance of
    :class:`werkzeug.wrappers.Response` and answer certain questions
    (eg. what methods are allowed?) or do tasks (delete the resource).

    This class is meant to be subclassed.
    """

    def __init__(self, req, rsp):
        "Initializes the object. The decision core does this on every request."
        pass

    def allowed_methods(self, req, rsp):
        "Returns a list of allowed methods."
        return ["GET", "HEAD"]

    def allow_missing_post(self, req, rsp):
        "Returns True if POST on URLs that don\'t exist yet is allowed."
        return False

    def auth_required(self, req, rsp):
        "Returns True if auth is required."
        return True

    def content_types_accepted(self, req, rsp):
        """
        Returns a list of accepted Content-Types. Each element of
        the list is a tuple that contains the type and a method
        or a function that parses content in that type. For example::

            return [
                ("application/json", self.from_json)
            ]
        """
        return None

    def content_types_provided(self, req, rsp):
        """
        Returns a list of provided Content-Types. Each element of
        the list is a tuple that contains the type and a method
        or a function that converts content to that type. For example::
        
            return [
                ("application/json", self.to_json)
            ]
        """
        return [
            ("text/html", self.to_html)
        ]

    def created_location(self, req, rsp):
        "Returns the Location of a created resource."
        return None

    def delete_completed(self, req, rsp):
        "Returns True if deletion is completed."
        return True

    def delete_resource(self, req, rsp):
        "Deletes the resource."
        return False

    def expires(self, req, rsp):
        "Returns the Expires header value."
        return None

    def forbidden(self, req, rsp):
        "Returns True if access is forbidden."
        return False

    def generate_etag(self, req, rsp):
        "Returns the ETag header value."
        return None

    def is_authorized(self, req, rsp):
        """
        Returns True if current user is authorized to access this
        resource. Don't forget you can have logic here.
        """
        return True

    def is_conflict(self, req, rsp):
        "Returns True if there is a conflict"
        return False

    def known_content_type(self, req, rsp):
        return True

    def known_methods(self, req, rsp):
        """
        Returns a set of known HTTP methods. You usually don't need to
        override this method.
        """
        return set([
            "GET", "HEAD", "POST", "PUT", "DELETE",
            "TRACE", "CONNECT", "OPTIONS"
        ])

    def languages_provided(self, req, rsp):
        """
        Returns a list of provided languages, eg. ["en", "ru", "en-us"].
        Returning None short circuits language negotiation.
        """
        return None

    def last_modified(self, req, rsp):
        "Returns the Last-Modified header value."
        return None

    def malformed_request(self, req, rsp):
        "Returns True if the request is malformed, eg. invalid JSON."
        return False

    def moved_permanently(self, req, rsp):
        """
        Returns a URL of the new location if the resource is moved permanently.
        Otherwise, returns False.
        """
        return False

    def moved_temporarily(self, req, rsp):
        """
        Returns a URL of the new location if the resource is moved temporarily.
        Otherwise, returns False.
        """
        return False

    def multiple_choices(self, req, rsp):
        "Returns True if there are multiple choices for current request."
        return False

    def options(self, req, rsp):
        "Returns a list of (header, value) pairs to set on OPTIONS requests."
        return []

    def post_is_create(self, req, rsp):
        "Returns True if POST creates a resource."
        return False

    def previously_existed(self, req, rsp):
        "Returns True if the resource previously existed."
        return False

    def process_post(self, req, rsp):
        """
        Processes POST requests.
        Only executed if post_is_create returns False.
        """
        return False

    def resource_exists(self, req, rsp):
        "Returns True if the resource exists."
        return True

    def service_available(self, req, rsp):
        "Returns True if the service is avaliable."
        return True

    def uri_too_long(self, req, rsp):
        "Returns True if the request URI is too long."
        return False

    def valid_content_headers(self, req, rsp):
        "Returns True if the Content-* headers are valid."
        return True

    def valid_entity_length(self, req, rsp):
        "Returns True if the entity length is valid."
        return True

    def variances(self, req, rsp):
        """
        Returns a list of variances (for the Vary HTTP header), eg.
        ["Accept-Something"]. Don't include "Accept" or "Accept-Language" here!
        These are included automatically if content_types_provided and/or
        languages_provided return more than one item.
        """
        return []
