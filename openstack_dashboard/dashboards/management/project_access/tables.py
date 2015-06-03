from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from openstack_dashboard.api import keystone
from openstack_dashboard.dashboards.management.project_access.send_email \
    import send_email

class RequestNewTenant(tables.LinkAction):
    name ="create"
    verbose_name=_("Create Project")
    url = "horizon:management:project_access:create"
    classes = ("ajax-modal", "btn-create")

#class RequestAccess(tables.UpdateAction):
#    """
#    Doesn't Work; however, this is
#    the proper way to do this
#    """
#    data_type_singular = _("Project")
#    data_type_plural = _("Projects")
#    name = "request_access" #Used internally
#    policy_rules=()
#    attrs = {"class":"btn-edit"}
#    classes = ("btn-edit")
#
#    def action_past(count):
#        return _("Requesting access for %s projects" % count)
#    #attrs = {'action':'Send Request', "data-foo":"bars"}
#
#    def allowed(self, request, datum):
#        print datum
#        return True
#
#    def action(self, request, datum_id, *args ):
#    #def update_cell(self, request, datum, obj_id, *args ):
#        print "In update"
#        print request, datum_id

class RequestJoin(tables.DeleteAction):
    """
    This approach is a hack, should inherit from 
    tables.UpdateAction instead
    """
    name = "join"
    data_type_singular = " "
    data_type_plural = " "
    
    action_present = "Request To Join"
    action_past = "Join Request Sent"
    classes = ('btn-success',)

    def action(self, request, project_id):
        """
        Sends email to admin 
        """

        all_tenants = keystone.list_projects()
        project_name = filter(lambda tenant: tenant.id == project_id, 
            all_tenants)[0].name
        
        
        msg_dict = {'username':request.user.username,
                    'user_id':request.user.id,
                    'project':project_name,
                    'project_id':project_id}

        send_email("join", msg_dict)
    
    def allowed(self, request, datum):
        conn = keystone.keystoneclient(request)
        my_tenants = conn.tenants.list()
        #all_tenants = keystone.list_projects()
        for tenant in my_tenants:
            if tenant.id == datum.id:
                return False
        return True

    def delete(self, request, obj_id):
        pass


class RequestLeave(tables.DeleteAction):
    """
    """
    name = "leave"
    data_type_singular = " "
    data_type_plural = " "
    
    action_present = "Request To Leave"
    action_past = "Request Submitted"

    def action(self, request, project_id):
        """
        Sends email to admin 
        """
        all_tenants = keystone.list_projects()
        project_name = filter(lambda tenant: tenant.id == project_id, 
            all_tenants)[0].name
        
        msg_dict = {'username':request.user.username,
                    'user_id':request.user.id,
                    'project':project_name,
                    'project_id':project_id}

        send_email("leave", msg_dict)
    
    def allowed(self, request, datum):
        conn = keystone.keystoneclient(request)
        my_tenants = conn.tenants.list()
        #all_tenants = keystone.list_projects()
        for tenant in my_tenants:
            if tenant.id == datum.id:
                return True 
        return False

    def delete(self, request, obj_id):
        pass

class RequestAccessTable(tables.DataTable):
    """
    Creates a table with the column name
    and a column with the actions
    """
    name = tables.Column("name",
                         verbose_name=_("Name"),)
    
    class Meta:
        name = "project_access"
        verbose_name = _("Project Access")
        table_actions = (RequestNewTenant, )
        row_actions = (RequestJoin, RequestLeave, )

