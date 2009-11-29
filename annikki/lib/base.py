"""The base Controller API

Provides the BaseController class for subclassing.
"""

from pylons.controllers import WSGIController
from pylons.templating import render_genshi as render
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from annikki import model
from annikki.model import meta

from authkit.permissions import ValidAuthKitUser
from authkit.authorize.pylons_adaptors import authorize

import json
from urllib import unquote

from decorator import decorator

import logging
log = logging.getLogger(__name__)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()


UserAuth = ValidAuthKitUser()

def serialize_json(self, f):
        body = unquote(request.body)
        #if body[-1:] == "=":
        #    body = body[:-1]
        try:
            data = json.loads(body)
            return json.dumps(f(self, data))
        except ValueError, e:
            log.debug(e)
            log.debug(body)
            abort(400, comment="The request body is not valid JSON")

def api_call(f):
    f1 = lambda s: serialize_json(s, f)
    f2 = authorize(UserAuth)(f1)
    return f2

