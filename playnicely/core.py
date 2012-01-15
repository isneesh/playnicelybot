
class PlayNicelyCommand(object):
    """Base command object. Deals with URLs and converting the JSON response into something more usable"""
    resource = None
    def __init__(self, request):
        self.request = request
    
    def call_url(self, command, *args, **kwargs):
        url = self.url % args
        
        return self.make_request(url, command, **kwargs)
    
    def make_request(self, url, command, **kwargs):
        
        post_data = kwargs.pop("post_data", {}) 
        
        method = kwargs.pop("method", "GET")
        
        detail = kwargs.pop("detail", None)
        
        if command != None:
            url = "%s/%s/" % (url, command)
        
        if detail:
            url = self._add_url_params(url, {"detail":detail})
        
        if method == "POST":
            response = self.request.post(url, **post_data)
        else:
            response = self.request.get(url)
        
        return response
    
    def _add_url_params(self, url, dict_):
        url += "?"
        for key in dict_.keys():
            url += "%s=%s" % (key, dict_[key])
        
        return url
    
    def get_resource(self, *args, **kwargs):
        url = self.resource_url % args
        
        response = self.make_request(url, "show", **kwargs)
        
        # do some conversion foo here (as long as we have a resource and we are not getting IDs)
        if self.resource and kwargs.get("detail", None) != "id":
            return self.resource(response)
        
        return response
    
    def get_resources(self, command, *args, **kwargs):
        url = self.url % args
        response = self.make_request(url, command, **kwargs)
        
        # do some conversion foo here (as long as we have a resource and we are not getting IDs)
        if self.resource and kwargs.get("detail", None) != "id":
            results = list()
            for item in response:
                results.append(self.resource(item))
            
            return results
        
        # just return the response
        return response

class PlayNicelyResource(object):
    
    def __init__(self, json={}):
        self.attrs = []
        for k in self.__class__.__dict__:
            if type(getattr(self, k)) == PlayNicelyAttribute:
                if json.get(k):
                    setattr(self, k, json[k])
                    self.attrs.append(k)
        
        super(PlayNicelyResource, self).__init__()
    
    def __repr__(self):
        out = {}
        for k in self.attrs:
            out[k] = getattr(self, k)
        return str(out)
    __str__ = __repr__

class PlayNicelyAttribute(object):
    pass