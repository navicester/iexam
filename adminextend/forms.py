from django import forms
from django.forms.models import BaseFormSet
from django.forms.formsets import formset_factory

from django.contrib import admin  
#from django.contrib.admin.options import helpers
from django.contrib.admin import helpers
from django.utils.html import escape
from django.db import models

'''
from django.forms.models import modelformset_factory
import copy
'''

class LinkFormAdminForm(forms.Form): #REF : InlineAdminForm
    class Meta:
        model = None
        back_field = [
        ]

    def get_back_array(self, instance):
        array= []
        if instance:
            model = instance.__class__
            for field_name in self.Meta.back_field:
                if field_name in model._meta.get_all_field_names():
                    field = model._meta.get_field(field_name)
                    array.append(field_name)
                    text = getattr(instance, field_name)
                    if isinstance(field,models.TextField):
                       text = text.replace('\r\n',"brbr")
                    array.append(escape(text))

        return array


class LinkFormFormset(BaseFormSet): #REF BaseInlineFormSet(BaseModelFormSet):
    pass 


class LinkFormAdminFormset(object): #REF :  class InlineAdminFormSet(object):

    prefix = []
    
    def __init__(self, formset , link = None, prefix=None, extra = 3, can_delete = False):
        self.formset = formset
        self.opts = link
        self.prefix = prefix
        self.link_m2m = False    
        self.link_init_search = False

    def __iter__(self):  
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
    