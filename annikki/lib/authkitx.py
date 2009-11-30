"""\
"""
import logging, cStringIO
log = logging.getLogger(__name__)

from pprint import pprint

from paste.httpexceptions import HTTPBadRequest
from paste.httpheaders import *
from authkit.authenticate.multi import MultiHandler, status_checker
from authkit.authenticate import get_template, valid_password, \
   get_authenticate_function, strip_base, RequireEnvironKey, \
   AuthKitUserSetter, AuthKitAuthHandler

from authkit.permissions import AuthKitConfigError

import simplejson as json

class JsonAuthenticator(object):
    """
    """
    type = 'json'
    def __init__(self,authfunc):
        self.authfunc = authfunc

    def authenticate(self, environ):
        try:
            try:
                body = environ['wsgi.input'].getvalue()
            except AttributeError:
                body = environ['wsgi.input'].read()
            data = json.loads(body)
            environ['wsgi.input']=cStringIO.StringIO(body)
        except ValueError:
            return HTTPBadRequest()
        username, password = data['user'], data['pwd']
        if username and password:
            if self.authfunc(environ, username, password):
                return username

    __call__ = authenticate


class JsonAuthHandler(AuthKitAuthHandler):
    """

    Parameters:

        ``application``

            The application object is called only upon successful
            authentication, and can assume ``environ['REMOTE_USER']``
            is set.  If the ``REMOTE_USER`` is already set, this
            middleware is simply pass-through.

        ``authfunc``

            This is a mandatory user-defined function which takes a
            ``username`` and ``password`` for its first and second
            arguments respectively.  It should return ``True`` if
            the user is authenticated.

    """
    def __init__(self, application, authfunc):
        self.application = application
        self.authenticate = JsonAuthenticator(authfunc)

    def __call__(self, environ, start_response):
        result = self.authenticate(environ)
        return result.wsgi_application(environ, start_response)

class JsonUserSetter(AuthKitUserSetter):
    def __init__(self, application, authfunc, users):
        self.application = application
        self.users = users
        self.authenticate = JsonAuthenticator(authfunc)

    def __call__(self, environ, start_response):
        environ['authkit.users'] = self.users
        result = self.authenticate(environ)
        if isinstance(result, str):
            AUTH_TYPE.update(environ, 'json')
            REMOTE_USER.update(environ, result)
        return self.application(environ, start_response)

def load_json_config(
    app,
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.json',
):
    auth_handler_params = {}
    user_setter_params = {}

    authenticate_conf = strip_base(auth_conf, 'authenticate.')
    app, authfunc, users = get_authenticate_function(
        app, 
        authenticate_conf, 
        prefix=prefix+'authenticate.', 
        format='basic'
    )
    auth_handler_params['authfunc'] = authfunc
    user_setter_params['authfunc'] = authfunc
    user_setter_params['users'] = users
    return app, auth_handler_params, user_setter_params

def make_json_auth_handler(
    app,
    auth_conf, 
    app_conf=None,
    global_conf=None,
    prefix='authkit.json',
):
    app, auth_handler_params, user_setter_params = load_json_config(
        app,
        auth_conf, 
        app_conf=None,
        global_conf=None,
        prefix='authkit.json', 
    )
    #app = MultiHandler(app)

    #def test_content_type(environ, status, headers):
    #    print repr(headers)
    #    for (key,val) in headers:
    #        if key.lower() == 'content-type':
    #            if val.lower() == "application/json" or val.lower() == 'application/jsonrequest':
    #                log.debug("Status checker returns True")
    #                return True
    #    log.debug("Status checker returns False")
    #    return False

    #app.add_method(
    #    'json', 
    #    JsonAuthHandler, 
    #    auth_handler_params['authfunc']
    #)
    #app.add_checker('json', test_content_type)
    app = JsonUserSetter(
        app,
        user_setter_params['authfunc'],
        user_setter_params['users'],
    )
    return app
