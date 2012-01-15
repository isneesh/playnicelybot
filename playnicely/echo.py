from playnicely.core import PlayNicelyCommand


class Echo(PlayNicelyCommand):
    url = ""
    
    def __init__(self, request):
        self.request = request
    
    def call(self):
        raise NotImplemented()
        self.call_url("echo")