from playnicely.core import PlayNicelyCommand, PlayNicelyResource, PlayNicelyAttribute

from playnicely.projects import Project

class User(PlayNicelyResource):
    username = PlayNicelyAttribute()
    user_id = PlayNicelyAttribute()
    first_name = PlayNicelyAttribute()
    surname = PlayNicelyAttribute()
    image = PlayNicelyAttribute()
    
    project_ids = PlayNicelyAttribute()
    updated_at = PlayNicelyAttribute()
    created_at = PlayNicelyAttribute()

class Users(PlayNicelyCommand):
    resource_url = "/user/%s"
    url = "/user"
    resource = User
    
    def show(self, user_id, detail="compact"):
        return self.get_resource(user_id, detail=detail)
    
    def list_projects(self, user_id, detail="compact"):
        response = self.make_request("/user/%s/project" % user_id, "list", detail=detail)
        
        results = list()
        for item in response:
            results.append(Project(item))
        
        return results
        
    

