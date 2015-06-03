from horizon import exceptions
from horizon import forms
from django.utils.translation import ugettext_lazy as _
from horizon import messages 

from openstack_dashboard.dashboards.management.project_access.send_email \
    import send_email

class RequestNewTenantForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length="255", label=_("Name"), required=True)
    description = forms.CharField(widget=forms.widgets.Textarea(
        attrs={'class': 'modal-body-fixed-width'}),
        label=_("Description"),
        required=True)
    
    principal = forms.CharField(max_length="255", label=_("Principal"), required=True)
    institution = forms.CharField(max_length="255", label=_("Institution"), required=True)

    def __init__(self, request, *args, **kwargs):
        super(RequestNewTenantForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        #Clean the data before handling it
        data = super(RequestNewTenantForm, self).clean()
        return data

    def handle(self, request, data):
        """Send the email"""
        msg_dict = {'username': request.user.username,
                     'user_id': request.user.id,
                     'project':data["name"],
                     'description':data["description"],
                     'institution':data["institution"],
                     'principal':data["principal"]}
        send_email("new", msg_dict)
        
        messages.success(request,
             _('Your request has been submitted') )
        return True 
