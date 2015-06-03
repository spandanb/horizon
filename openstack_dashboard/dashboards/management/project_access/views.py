# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings

from openstack_dashboard.dashboards.management.project_access\
    import forms as project_forms
from openstack_dashboard.dashboards.management.project_access\
    import tables as project_tables

from openstack_dashboard.api import keystone
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy, reverse
from horizon import tables
from horizon import forms


class IndexView(tables.DataTableView):
    table_class = project_tables.RequestAccessTable
    template_name = 'management/project_access/index.html'

    def get_data(self):
            #Gets list of tenants
            all_tenants = keystone.list_projects()
            #Tenants not to be seen
            black_list = ["invisible_to_admin", "admin", "security", "service", "savi", "havana"]
            
            #Tenants to be seen
            white_list = []

            for tenant in all_tenants:
                if tenant.name not in black_list:
                    white_list.append(tenant)

            return white_list

class RequestNewTenantView(forms.ModalFormView):
    form_class = project_forms.RequestNewTenantForm 
    template_name = 'management/project_access/new_project.html'
    context_object_name = 'tenant'
    success_url = reverse_lazy("horizon:management:project_access:index") 

