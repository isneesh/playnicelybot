VERSION = (0, 1, 1)
__doc__ = "PlayNice.ly API v1 library for Python"
__author__ = "Rob Hudson"
__contact__ = "rob@playnice.ly"
__homepage__ = "http://github.com/playnicely/python-playnicely"
__version__ = ".".join(map(str, VERSION))

try:
    import json as simplejson  # For Python 2.6
except ImportError:
    import simplejson

class BaseError(Exception):
    def __init__(self, e):
        super(BaseError, self).__init__()
        self.code = e.code
        try:
            data = e.read()
            if len(data) > 0:
                json = simplejson.loads(data)
                self.args = (json["error_message"],)
                self.type = json["type"]
        except (ValueError, AttributeError):
            pass

class ApiError(BaseError):
    pass

class AuthenticationError(BaseError):
    pass

class RequestError(BaseError):
    pass

class NotFoundError(BaseError):
    pass

class BadHttpMethodError(BaseError):
    pass

class ServerError(BaseError):
    pass

class ApiUnavailable(BaseError):
    pass

class RateLimitReached(Exception):
    def __init__(self, e, retry_after):
        super(RateLimitReached, self).__init__(e)
        self.retry_after = retry_after
