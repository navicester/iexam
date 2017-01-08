from django import forms
from django.forms.models import BaseFormSet
from django.forms.formsets import formset_factory

###########################################################################
#
#               LinkFormAdminFormset / LinkFormAdminForm / LinkFormAdmin
#
###########################################################################


class LinkFormAdminFormset(object): #REF :  class InlineAdminFormSet(object):

    prefix = []
    
    def __init__(self, formset , prefix=None, extra = 3, can_delete = False):
        self.formset = formset
        self.prefix = prefix
        self.link_m2m = False    
        self.link_init_search = False

    def __iter__(self):  #return to {% for form in LinkFormAdminFormset %}
        for form in self.formset.initial_forms:
            yield form
        for form in self.formset.extra_forms:
            yield form
            
        yield self.formset.empty_form    

    def fields(self):
#        return self.formset.form.base_fields
        for field in self.formset.form.base_fields:
            yield self.formset.form.base_fields[field]

    def get_fk(self,formset):
        return getattr(formset, "fk", None)

class LinkFormFormset(BaseFormSet): #REF BaseInlineFormSet(BaseModelFormSet):
    pass 
    
class LinkFormAdminForm(forms.Form): #REF : InlineAdminForm
    pass


class LinkFormAdmin(object):
    link_form = None
    link_obj_class = None
    link_m2m = False
    link_init_search = False    
    
    extra = 0
    max_num = None
    can_delete = True
    can_order = True
    
#    parent = None

    def get_formset(self, request, obj=None, **kwargs):
        defaults = {
            "extra": self.extra,
            "max_num": self.max_num,
            "can_delete": self.can_delete,
            "can_delete": self.can_order,            
        }

        defaults.update(kwargs)
        
        return formset_factory(form = self.link_form, formset = LinkFormFormset, **defaults)
#        return formset_factory(form = self.link_form, formset = LinkFormFormset, extra = self.extra, can_delete = self.can_delete, can_order = self.can_order)

    def has_add_permission(self, request):
        return True
        '''
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_add_permission())
        '''
    def has_change_permission(self, request, obj=None):
        return True
        '''
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())
        '''
        
    def has_delete_permission(self, request, obj=None):
        return True
        '''
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission())
        '''
        
