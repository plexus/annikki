"""
Extensions on top of httplib, most notably a HTTPClient that's well suited
to be used with REST style APIs.

HTTP return codes of 300 or more are reported as an exception.
"""

try:
    import httplib as http
except ImportError:
    #Python 3
    import http.client as http

from exceptions import Exception

"""
Exceptions
"""
class HTTPError(Exception):
    def __init__(self, status, body):
        self.status = status
        self.msg  = http.responses[status]
        self.body = body

    def __repr__(self):
        return "<HTTP %s %d %s>" % (self.__class__.__name__, self.status, self.msg)

    def __str__(self):
        return "%s (%d)" % (self.msg, self. status)

class RedirectError(HTTPError):
    pass
class ClientError(HTTPError):
    pass
class ServerError(HTTPError):
    pass

class Unauthorized(ClientError):
    pass

def http_error(code, body):
    if code == 401:
        return Unauthorized(code, body)
    elif code >= 300 and code < 400:
        return RedirectError(code, body)
    elif code >= 400 and code < 500:
        return ClientError(code, body)
    elif code >= 500 and code < 600:
        return ServerError(code, body)
    else:
        return HTTPError(code, body)

############################################################
#
class HTTPClient:
    def __init__(self, conn, protocol = 'http'):
        self.conn = conn
        self.protocol = protocol
        self.response = None

    def _request(self, method, path_info, body, headers):
        print(method, path_info, body, headers)
        url = "%s://%s%s" % (self.protocol, self.conn.host, path_info)
        try:
            self.conn.request(method, url, body, headers)
        except http.ImproperConnectionState, e:
            self.conn.close()
            self.conn.connect()
            print("retrying")
            self._request(method, path_info, body, headers)

        self.response = self.conn.getresponse()
        self.response.begin()
        body = self.response.read()
        print(self.response.status, body)
        if self.response.status >= 300:
            raise http_error(self.response.status, body)
        return body

    def get(self, path_info, headers = {}):
        reply = self._request('GET', path_info, None, headers)
        return self.unmarshal(reply)

    def post(self, path_info, data, headers = {}):
        reply = self._request('POST', path_info, self.marshal(data), headers)
        return self.unmarshal(reply)

    # 'marshal' and 'unmarshal' are called before sending/after receiving data.
    # Override them to use a specific representation format (XML/JSON/...)
    # or to do pre/post processing on the data

    def marshal(self, data):
        "Convert a Python object to a string representation to be sent over the wire"
        return data

    def unmarshal(self, body):
        "Convert a response body into a Python object"
        return body

    
    #TODO:
    #PUT, DELETE, HEAD


"""
import httplib as http
import httpx
import simplejson
ua = httpx.HTTPClient(http.HTTPConnection('www.arnebrasseur.net'), marshal=simplejson)
print repr(ua.get('/json'))
"""
