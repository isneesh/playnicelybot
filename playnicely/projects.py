from playnicely.core import PlayNicelyCommand, PlayNicelyResource, PlayNicelyAttribute

class Project(PlayNicelyResource):
    project_id = PlayNicelyAttribute()
    name = PlayNicelyAttribute()
    item_ids = PlayNicelyAttribute()
    user_ids = PlayNicelyAttribute()
    milestone_ids = PlayNicelyAttribute()
    
    updated_by = PlayNicelyAttribute()
    updated_at = PlayNicelyAttribute()
    created_by = PlayNicelyAttribute()
    created_at = PlayNicelyAttribute()

class Projects(PlayNicelyCommand):
    resource = Project
    url = "/project/"
    resource_url = "/project/%d"
    
    def show(self, project_id, detail="compact"):
        return self.get_resource(project_id, detail=detail)