from django.contrib import admin  
#from django.contrib.admin.options import helpers
from django.contrib.admin import helpers
'''
from django.forms.models import modelformset_factory
import copy
'''


###########################################################################
#
#               LinkModelAdminFormSet / LinkModelAdmin
#
###########################################################################



class LinkModelAdminFormSet(helpers.InlineAdminFormSet):
    link_m2m = False
    bLink = True


class LinkModelAdmin(admin.TabularInline):

    link_m2m = False
    obj_id = ''
    
    def __init__(self, parent_model, admin_site):
        self.admin_site = admin_site
        self.parent_model = parent_model
        self.opts = self.model._meta
        super(LinkModelAdmin, self).__init__(parent_model, admin_site)
        if self.verbose_name is None:
            self.verbose_name = self.model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = self.model._meta.verbose_name_plural

    '''
    def get_formset(self, request, obj=None, **kwargs):
        if self.declared_fieldsets:
            fields = ['id']
            fields_raw = flatten_fieldsets(self.declared_fieldsets)
            fields.append(fields_raw)
        else:
            fields = None

        my_context = {
            "fields": fields,
        }

        kwargs.update(my_context)

        return super(LinkModelAdmin, self).get_formset(request,obj = obj,**kwargs)
    '''
    