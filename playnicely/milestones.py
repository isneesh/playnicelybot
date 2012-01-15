from playnicely.core import PlayNicelyCommand, PlayNicelyResource, PlayNicelyAttribute

class Milestone(PlayNicelyResource):
    project_id = PlayNicelyAttribute()
    milestone_id = PlayNicelyAttribute()
    name = PlayNicelyAttribute()
    item_ids = PlayNicelyAttribute()
    
    updated_by = PlayNicelyAttribute()
    updated_at = PlayNicelyAttribute()
    created_by = PlayNicelyAttribute()
    created_at = PlayNicelyAttribute()

class Milestones(PlayNicelyCommand):
    resource_url = "/project/%d/milestone/%d"
    url = "/project/%d/milestone"
    resource = Milestone
    
    def show(self, project_id, milestone_id, detail="compact"):
        return self.get_resource(project_id, milestone_id, detail=detail)
        
    def list(self, project_id, detail="compact"):
        return self.get_resources("list", project_id, detail=detail)
    
