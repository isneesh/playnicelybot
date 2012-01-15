from projects import Projects
from items import Items
from echo import Echo
from users import Users
from milestones import Milestones

from request import PlayNicelyRequest


class PlayNicely(object):
    
    def __init__(self, username=None, password=None, access_token=None, request=None):
        
        self.request = request or PlayNicelyRequest(username, password)
        
        self.projects = Projects(self.request)
        self.milestones = Milestones(self.request)
        self.items = Items(self.request)
        self.users = Users(self.request)
        self.echo = Echo(self.request)