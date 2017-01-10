from django.contrib import admin
from django.contrib.admin.options import *
import time 

from .models import *
from .helpers_linkmodelform import LinkModelAdminFormSet
from .helpers_linkform import LinkFormAdminFormset

from django.db import transaction
csrf_protect_m = method_decorator(csrf_protect)

###########################################################################    
#
#               MyModelAdmin
#
###########################################################################

class MyModelAdmin(admin.ModelAdmin):

    bAllowAddLink = False

    modelform_links = []
    form_links = []
    self_form_link = None

    fieldsets_fk = ()

    ##### for LinkForm method#####
    def get_linkform_instances(self, request):
        linkinstances = []
        for form_link in self.form_links:
            linkinstance = form_link()
            linkinstances.append(linkinstance)
        return linkinstances


    def get_linkform_forms(self, request):
        form_links = []
        for form_link in self.form_links:
            form_links.append(form_link.link_form)
        return form_links


    def get_linkform_m2ms(self, request):
        linkm2ms = []
        for form_link in self.form_links:
            linkm2ms.append(form_link.link_m2m)
        return linkm2ms

    def get_linkform_initsearchs(self, request):
        linkinitsearchs = []
        for form_link in self.form_links:
            linkinitsearchs.append(form_link.link_init_search)
        return linkinitsearchs

    def get_linkform_models(self, request):
        linkmodels = []
        for form_link in self.form_links:
            linkmodels.append(form_link.link_obj_class)
        return linkmodels

    def get_linkform_formsets(self, request, obj=None):
        for link_instance in self.get_linkform_instances(request):
            if request:
                if not (link_instance.has_add_permission(request) or
                        link_instance.has_change_permission(request, obj) or
                        link_instance.has_delete_permission(request, obj)):
                    continue 
                if not link_instance.has_add_permission(request):
                    link_instance.max_num = 0
            yield link_instance.get_formset(request, obj)

        '''
        linkFromset = []
        for form_link in self.get_linkform_instances(request):
            linkFromset.append(form_link.get_formset(request, obj))
        return linkFromset
        '''

    def filter_objects(self, fk_model, LinkObjClass, obj):
        link_objs = None
        
        if  fk_model == Word:
            link_objs = LinkObjClass.objects.filter(word = obj)

        return link_objs
        
    def get_linkform_queryset_from_model(self, obj, LinkObjClass):

        fk_model = self.model        

# add_form_link

        return self.filter_objects(fk_model, LinkObjClass, obj)
    
    def get_linkform_formset_initial(self, request, object_id):

        obj = self.get_object(request, unquote(object_id))

        initials = []

        for LinkForm, LinkObjClass in zip(self.get_linkform_forms(request), self.get_linkform_models(request)):           
            link_objs = self.get_linkform_queryset_from_model(obj, LinkObjClass)
            initial = [] #list
            if link_objs != None:
                for link_obj in link_objs:
                    form = {} #dict
                    items = link_obj.getitems()
                    for field in LinkForm.base_fields:                    
                        form[field] = items[field]
                    initial.append(form)
            initials.append(initial)
            
        return initials

    def sort_linkform_formset(self, request, formset, is_add_view = False):
        # add view - POST data bottom to top
        # change view - POST data top to bottom
        
        for form in formset.forms:
            if len(form.cleaned_data) == 0  :
            #if not form.is_valid():
                formset.forms.remove(form)
                
        return formset
        

    ##### for Link(Model) method##### 
    def get_link_instances(self, request, obj=None):
        link_instances = []
        for modelform_link in self.modelform_links:
            link = modelform_link(self.model, self.admin_site)  
            if request:
                if not (link.has_add_permission(request) or
                        link.has_change_permission(request, obj) or
                        link.has_delete_permission(request, obj)):
                    continue 
                if not link.has_add_permission(request):
                    link.max_num = 0
            link_instances.append(link) 

        return link_instances

    def get_link_formsets(self, request, obj=None):
        for link in self.get_link_instances(request, obj):
            yield link.get_formset(request, obj)

    ############################
    def _save_obj(self, fk_model, link_obj, link_m2m, obj): # this function can change to global
        setattr(link_obj, fk_model._meta.object_name + "_id", obj._get_pk_val())
        if fk_model == Word:
            if link_m2m == False:
                link_obj.word = obj
            else:
                link_obj.word.add(obj)
                

# add_form_link
        '''
        if fk_model == lab_device_item:
            if link_m2m == False:
                link_obj.lab_device_item = obj
            else:
                link_obj.lab_device_item.add(obj)
        if fk_model == PC:
            if link_m2m == False:
                link_obj.PC = obj
            else:
                link_obj.PC.add(obj)
        if fk_model == UE:
            if link_m2m == False:
                link_obj.UE = obj
            else:
                link_obj.UE.add(obj)
        if fk_model == Platform:
            if link_m2m == False:
                link_obj.Platform = obj
            else:
                link_obj.Platform.add(obj)
        '''
            
        link_obj.save()
        
    def _delete_empty_objs(self, fk_model, linkobj, link_m2m):

        if link_m2m == False:
            self.filter_objects(fk_model, linkobj, None).delete()
            
            '''
            if fk_model == lab_device_item:                    
                linkobj.objects.filter(lab_device_item= None).delete()
            if fk_model == PC:                    
                linkobj.objects.filter(PC= None).delete()
            if fk_model == Platform:                    
                linkobj.objects.filter(Platform= None).delete()
            if fk_model == UE:                    
                linkobj.objects.filter(UE= None).delete()
            '''

    '''
    fk_model :  foreignkey or m2m model
    link_m2m : whether this is m2m relationship
    '''
    def _delete_obj(self, fk_model, link_obj, link_m2m, obj):

        if link_m2m == True:
            #fk = getattr(link_obj, fk_model._meta.many_to_many)
            fk = getattr(link_obj, fk_model._meta.object_name.lower())
            fk.remove(obj)
        else:
            setattr(link_obj, fk_model._meta.object_name + "_id", None)
            link_obj.save()

        '''
        Example:

        if fk_model == lab_device_item:
            if link_m2m == True:
                link_obj.lab_device_item.remove(obj)
            else:
                link_obj.delete()
        if fk_model == PC:
            if link_m2m == True:
                link_obj.PC.remove(obj)
            else:
                link_obj.delete()
        if fk_model == UE:
            if link_m2m == True:
                link_obj.UE.remove(obj)
            else:
                link_obj.delete()
        if fk_model == Platform:
            if link_m2m == True:
                link_obj.Platform.remove(obj)
            else:
                link_obj.delete()

        else:
            link_obj.delete()
        '''

    # is there a method to implement this functio without write the object name explicitly ?
    # should do this in subcass to help extend, write here for simpty !!! or change it to global
    def _delete_ghost_obj(self, request, obj):
            # workaround - Delete link_obj which ForeignKey is still Null
            # case 1 : user delete it in Parent page through X key in formset
            # case 2 : save link obj, but not save in parent, it will become ghost obj, this can be solve through save link obj in parent page or save parent first

            return 
            
            if self.form_links != []:
                link_models = copy.deepcopy(self.get_linkform_models(request))
                for linkobj, link_m2m in zip(link_models, self.get_linkform_m2ms(request)):
                    self._delete_empty_objs(self.model, linkobj, link_m2m)
                    
            if self.modelform_links != []:
                link_models = []
                for link in self.modelform_links:
                    link_models.append(link.model)
                for linkobj in link_models:
                    self._delete_empty_objs(self.model, linkobj, False)

    
    # should do this in subcass to help extend, write here for simpty !!!
    def _save_link_obj(self, request, obj, link_key = 'id'):
        if self.form_links != []:
            prefixes = {}
            for LinkForm, LinkObjClass, LinkObjFormSet, link_m2m in zip(self.get_linkform_forms(request), self.get_linkform_models(request), self.get_linkform_formsets(request), self.get_linkform_m2ms(request)):
                #prefix = LinkObjFormSet.get_default_prefix()
                prefix = LinkForm.Meta.class_name + "_set"                
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                formset = LinkObjFormSet(request.POST, request.FILES, prefix = prefix)
                for form in formset.forms:
                    if form.is_valid() and form.cleaned_data.has_key(link_key): 
                        link_obj_id = form.cleaned_data[link_key] #string
                        if link_obj_id.isdigit():
                            link_obj = LinkObjClass.objects.get(pk=link_obj_id)                            
                            if formset._should_delete_form(form):
                                self._delete_obj(self.model, link_obj, link_m2m, obj)
                                self.log_change(request, obj, '"'+force_text(link_obj)+'"' + ' deleted from  ' + '"' + force_text(obj) + '"')
                            else:
                                self._save_obj(self.model, link_obj, link_m2m, obj)
                                self.log_change(request, obj, '"'+force_text(link_obj)+'"' + ' add or modified in  ' + '"' + force_text(obj) + '"')
                                
        if self.modelform_links != []:  #only support ForeignKey inline
            link_instances = self.get_link_instances(request, None)          
            prefixes = {}
            for FormSet, link in zip(self.get_link_formsets(request), link_instances): 
                prefix = FormSet.get_default_prefix()   #need to change ??????????/
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=obj,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=link.queryset(request))

                for form in formset.forms:
                    form.is_valid()  # this line is to get cleaned_data, but for modelForm, it's invalid, reason is ObjectExist
                    if form.instance.id != '':
                        link_obj_id = form.instance.id
                        if link_obj_id > 0 : #integer
                            link_obj = link.model.objects.get(pk=link_obj_id)                            
                            if formset._should_delete_form(form):
                                self._delete_obj(self.model, link_obj, False, obj)
                            else:
                                self._save_obj(self.model, link_obj, False, obj)

    from django.core.context_processors import csrf
    from django.views.decorators.csrf import csrf_exempt
    @csrf_exempt

    def _dismiss_popup(self, request, obj):
        pk_value = obj._get_pk_val()
        
        from django.shortcuts import render_to_response
        from django.utils.html import escape, escapejs

        return render_to_response('admin/myprj/linkback.html', 
                                            {'array': self.self_form_link().get_back_array(obj), 
                                            'newId' : escape(pk_value), 
                                            'newRepr' : escape(obj),
                                            })

        
    '''
    def save_model(self, request, obj, form, change):
        self.bAllowAddLink = True
        super(MyModelAdmin, self).save_model(request,obj, form, change)
    '''
    
    def response_add(self, request, obj, post_url_continue=None):
        if request.method == "POST":
            self._save_link_obj(request,obj)            
            self._delete_ghost_obj(request,obj)

        if "_popup" in request.POST:
            return self._dismiss_popup(request, obj)            

        return super(MyModelAdmin, self).response_add(request,obj, post_url_continue)  

    def response_change(self, request, obj):
        if request.method == "POST":
            self._save_link_obj(request,obj)
            self._delete_ghost_obj(request,obj)
            
        if "_continue" in request.POST:
            return super(MyModelAdmin, self).response_change(request,obj) 
        elif "_saveasnew" in request.POST:
            return super(MyModelAdmin, self).response_change(request,obj) 
        elif "_addanother" in request.POST:
            return super(MyModelAdmin, self).response_change(request,obj) 
        else:
            if "_popup" in request.POST or "_popup" in request.GET:
                return self._dismiss_popup(request, obj)
            else:
                return super(MyModelAdmin, self).response_change(request,obj) 

        return super(MyModelAdmin, self).response_change(request,obj)          

    def export_all(self, request, queryset):
        pass

    def import_all(self, request, queryset):
        pass

    def my_get_fieldsets(self, request, obj=None):
        if not ("_popup" in request.POST or "_popup" in request.GET):
            add_fieldsets = []
            add_fieldsets = copy.deepcopy(self.fieldsets)
            if self.fieldsets_fk != ():
                add_fieldsets.append(self.fieldsets_fk)
            return add_fieldsets
        else:
            return self.fieldsets

    def get_fieldsets(self, request, obj=None):
        if self.my_get_fieldsets(request):
            return self.my_get_fieldsets(request)

        return super(MyModelAdmin, self).get_fieldsets(request,obj)

    def get_form(self, request, obj=None, **kwargs):
        if self.my_get_fieldsets(request):
            fields = flatten_fieldsets(self.my_get_fieldsets(request))
        else:
            fields = None

        my_context = {
            "fields": fields,
        }

        kwargs.update(my_context)

        return super(MyModelAdmin, self).get_form(request,obj = obj,**kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        if self.my_get_fieldsets(request):
            fields = flatten_fieldsets(self.my_get_fieldsets(request))
        else:
            fields = None

        my_context = {
            "fields": fields,
        }

        kwargs.update(my_context)

        return super(MyModelAdmin, self).get_formset(request,obj = obj,**kwargs)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            pass

        action_form = self.action_form(data, auto_id=None)
        action_form.fields['action'].choices = self.get_action_choices(request)

        # If the form's valid we can handle the action.
        if action_form.is_valid():
            action = action_form.cleaned_data['action']
            if action == 'export_all':
                return self.export_all(request, None)
            if action == 'import_all':
                return self.import_all(request, None)
        return super(MyModelAdmin, self).changelist_view( request, extra_context)
              
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):

        if not self.has_add_permission(request):
            raise PermissionDenied

        # LineInlineFormAdimin
        link_admin_obj_formset = None
        link_admin_obj_formsets = []
        self.bAllowAddLink = False

        if self.form_links != []:
            prefixes = {}
            for LinkForm, LinkMany2Many, LinkInitSearch, LinkObjFormSet in zip(self.get_linkform_forms(request), self.get_linkform_m2ms(request), self.get_linkform_initsearchs(request), self.get_linkform_formsets(request)):   
                #prefix = LinkObjFormSet.get_default_prefix()
                prefix = LinkForm.Meta.class_name + "_set"
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                if request.method == "POST":                
                    formset = LinkObjFormSet(request.POST, request.FILES, prefix = prefix)                    
                    if formset.is_valid():
                        formset = self.sort_linkform_formset(request, formset, True)
                        link_admin_obj_formset = LinkFormAdminFormset(formset = formset)
                    else:
                        link_admin_obj_formset = LinkFormAdminFormset(formset = LinkObjFormSet(prefix = prefix))
                else:
                    link_admin_obj_formset = LinkFormAdminFormset(formset = LinkObjFormSet(prefix = prefix))
                    
                link_admin_obj_formset.link_m2m = LinkMany2Many
                link_admin_obj_formset.link_init_search = LinkInitSearch                
                link_admin_obj_formsets.append(link_admin_obj_formset)

            extra_context_cur = {        
                'link_form_admin_formsets':link_admin_obj_formsets,      
                'bAllowAddLink': self.bAllowAddLink,
            }

            if extra_context == None:
                extra_context = {}

            extra_context.update(extra_context_cur)

        if self.modelform_links != []:
            # LineInlineModelAdimin
            #model = self.model
            #opts = model._meta

            formsets = []
            link_instances = self.get_link_instances(request, None)  

            if request.method == 'POST':
                new_object = self.model()
                prefixes = {}
                for FormSet, link in zip(self.get_link_formsets(request), link_instances): 
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(data=request.POST, files=request.FILES,
                                      instance=new_object,
                                      save_as_new="_saveasnew" in request.POST,
                                      prefix=prefix, queryset=link.queryset(request))
                    formsets.append(formset)
            else:
                prefixes = {}
                for FormSet, link in zip(self.get_link_formsets(request), link_instances):  
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(instance=self.model(), prefix=prefix,
                                      queryset=link.queryset(request))
                    formsets.append(formset)

            link_admin_formsets = []
            link_media = self.media #should implement it for further dev !!!!
            for link, formset in zip(link_instances, formsets):
                fieldsets = list(link.get_fieldsets(request))
                readonly = list(link.get_readonly_fields(request))
                prepopulated = dict(link.get_prepopulated_fields(request))
                link_admin_formset = LinkModelAdminFormSet(link, formset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                link_admin_formset.link_m2m = link.link_m2m
                link_admin_formsets.append(link_admin_formset)
                
            context_tmp = {
                'link_admin_formsets': link_admin_formsets,
                'link_media':link_media,
            }

            if extra_context == None:
                extra_context = {}        
            extra_context.update(context_tmp or {})   

        extra_auto = {
            'is_add_new':'True',
            'CreateTime': time.strftime("%H:%M:%S") ,
            'CreateDate':time.strftime("%Y-%m-%d")  
        }        

        if extra_context == None:
            extra_context = {}        
        extra_context.update(extra_auto or {})   
        
        return super(MyModelAdmin, self).add_view(request,form_url,extra_context)

        
    @csrf_protect_m
    @transaction.atomic
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            self.bAllowAddLink = False
        else:
            self.bAllowAddLink = True

        if self.form_links != []:
            initial = self.get_linkform_formset_initial(request,object_id)
            link_admin_obj_formsets = []

            prefixes = {}
            for LinkInitial, LinkForm, LinkObjFormSet, link_m2m, link_initsearch in zip(initial, self.get_linkform_forms(request), self.get_linkform_formsets(request), self.get_linkform_m2ms(request), self.get_linkform_initsearchs(request)): 
                #prefix = LinkObjFormSet.get_default_prefix()
                prefix = LinkForm.Meta.class_name + "_set"                
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                if request.method == "POST":                          
                    formset = LinkObjFormSet(request.POST, request.FILES, prefix = prefix) 
                    if formset.is_valid():
                        formset = self.sort_linkform_formset(request, formset)
                        link_admin_obj_formset = LinkFormAdminFormset(formset = formset)                    
                    else:
                        link_admin_obj_formset = LinkFormAdminFormset(formset = LinkObjFormSet(prefix = prefix))

                else:
                    link_obj_formset = LinkObjFormSet(initial = LinkInitial, prefix = prefix)
                    link_admin_obj_formset = LinkFormAdminFormset(formset = link_obj_formset)
                    
                link_admin_obj_formset.link_m2m = link_m2m
                link_admin_obj_formset.link_init_search = link_initsearch                
                link_admin_obj_formsets.append(link_admin_obj_formset)                
        
            extra_context_cur = {        
                'link_form_admin_formsets':link_admin_obj_formsets,      
                'bAllowAddLink': self.bAllowAddLink,
            }

            if extra_context == None:
                extra_context = {}

            extra_context.update(extra_context_cur)

        # link admin
        ##########################################################

        if self.modelform_links != []:
            model = self.model
            opts = model._meta

            obj = self.get_object(request, unquote(object_id))
            
            if request.method == 'POST' and "_saveasnew" in request.POST:
                return self.add_view(request, form_url=reverse('admin:%s_%s_add' %
                                        (opts.app_label, opts.module_name),
                                        current_app=self.admin_site.name))

            ModelForm = self.get_form(request, obj)
            formsets = []
            link_instances = self.get_link_instances(request, obj)
            if request.method == 'POST':
                form = ModelForm(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    form_validated = True
                    new_object = self.save_form(request, form, change=True)
                else:
                    form_validated = False
                    new_object = obj

                prefixes = {}
                for FormSet, link in zip(self.get_link_formsets(request, new_object), link_instances):
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(request.POST, request.FILES,
                                      instance=new_object, prefix=prefix,
                                      queryset=link.queryset(request))

                    formsets.append(formset)
                    
                if form_validated:
                    pass
            else:
                prefixes = {}
                for FormSet, link in zip(self.get_link_formsets(request, obj), link_instances):
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(instance=obj, prefix=prefix,
                                      queryset=link.queryset(request))
                    formsets.append(formset)

            link_admin_formsets = []
            for link, formset in zip(link_instances, formsets):
                fieldsets = list(link.get_fieldsets(request, obj))
                readonly = list(link.get_readonly_fields(request, obj))
                prepopulated = dict(link.get_prepopulated_fields(request, obj))
                link_admin_formset = LinkModelAdminFormSet(link, formset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                link_admin_formset.link_m2m = link.link_m2m                
                link_admin_formset.obj_id = object_id
                link_admin_formsets.append(link_admin_formset)

            context_tmp = {
                'link_admin_formsets': link_admin_formsets,
            }

            if extra_context == None:
                extra_context = {}
            
            extra_context.update(context_tmp or {})

        return super(MyModelAdmin, self).change_view(request,object_id, form_url,extra_context)

