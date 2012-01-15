import urllib2
import urllib

from playnicely import simplejson, ApiError, AuthenticationError, RequestError, NotFoundError, BadHttpMethodError, ServerError, ApiUnavailable, RateLimitReached

PLAYNICELY_URL = "https://api.playnice.ly/v1"

class PlayNicelyRequest(object):
    """Makes the actual call. Deals with low level errors, authentication and HTTP"""
    playnicely_url = PLAYNICELY_URL
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get(self, *path_components):
        path_components = filter(None, path_components)
        return self.make_request("/".join(path_components))
    
    def post(self, *path_components, **extra_post_data):
        path_components = filter(None, path_components)
        return self.make_request("/".join(path_components), extra_post_data,
            method="POST")
    
    def make_request(self, path, extra_post_data=None, method="GET"):
        
        extra_post_data = extra_post_data or {}
        url = "/".join([self.playnicely_url, path.lstrip("/")])
        result = self.raw_request(url, extra_post_data, method=method)
        
        return result
    
    def raw_request(self, url, post_data=None, method="GET"):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        passman.add_password(None, url, self.username, self.password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which `theurl` is a super-url
        
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # create the AuthHandler
        
        opener = urllib2.build_opener(authhandler)
        
        if post_data:
            json_data = simplejson.dumps(post_data)
            request = urllib2.Request(url, json_data, headers=self.http_headers)
        else:
            request = urllib2.Request(url, headers=self.http_headers)

        try:
            
            response = opener.open(request)
        except urllib2.HTTPError as e:
            self.handle_error(url, e)
        
        data = response.read()
        
        if len(data) > 0:
            return simplejson.loads(data)
        else:
            return True
    
    def handle_error(self, url, error):
        if error.code == 401:
            raise AuthenticationError(error)
        elif error.code == 400:
            raise RequestError(error)
        elif error.code == 404:
            raise NotFoundError(error)
        elif error.code == 406:
            raise BadHttpMethodError(error)
        elif error.code == 500:
            raise ServerError(error)
        elif error.code == 503:
            if "Retry-After" in error.headers:
                retry_after = int(error.headers["Retry-After"])
                raise RateLimitReached("Rate limit reached. Retry after %s seconds" % retry_after, retry_after=retry_after)
            else:
                raise ApiUnavailable(error)
        else:
            raise ApiError(error)
    
    @property
    def http_headers(self):
        return {"User-Agent": "playnicely v1",
                "Accept-Encoding": "application/json"}
    

