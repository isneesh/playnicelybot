from playnicely.core import PlayNicelyCommand, PlayNicelyResource, PlayNicelyAttribute

class Item(PlayNicelyResource):
    item_id = PlayNicelyAttribute()
    project_id = PlayNicelyAttribute()
    milestone_id = PlayNicelyAttribute()
    subject = PlayNicelyAttribute()
    body = PlayNicelyAttribute()
    type_name = PlayNicelyAttribute()
    status = PlayNicelyAttribute()
    
    updated_by = PlayNicelyAttribute()
    updated_at = PlayNicelyAttribute()
    created_by = PlayNicelyAttribute()
    created_at = PlayNicelyAttribute()
    tags = PlayNicelyAttribute()
    activity = PlayNicelyAttribute()
    involved = PlayNicelyAttribute()
    responsible = PlayNicelyAttribute()

class Items(PlayNicelyCommand):
    resource_url = "/project/%d/item/%d"
    url = "/project/%d/item"
    resource = Item
    
    def show(self, project_id, item_id, detail="compact"):
        return self.get_resource(project_id, item_id, detail=detail)
    
    def create(self, project_id, **data):
        return self.call_url("create", project_id, method="POST", post_data=data)
    
    def list(self, project_id, detail="compact"):
        return self.get_resources("list", project_id, detail=detail)
    
    def update(self, project_id, item_id, **data):
        return self.make_request(self.resource_url % (project_id, item_id), "update", method="POST", post_data=data)

