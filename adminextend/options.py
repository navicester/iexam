from django.contrib import admin
from django.contrib.admin.options import *
import time 

from .models import *
from .forms import LinkModelAdminFormSet, LinkFormAdminFormset, LinkFormFormset
from django.forms.models import modelformset_factory, formset_factory

from django.db import transaction
csrf_protect_m = method_decorator(csrf_protect)

###########################################################################    
#
#               MyModelAdmin
#
###########################################################################

class MyModelAdmin(admin.ModelAdmin):

    """
    class Media:
        css = {
            "all": ("my_styles.css",)
        }
        js = ("my_code.js",)
    """
    
    is_add_link_allowed = False

    modelform_links = []
    form_links = []
    self_form_link = None

    fieldsets_fk = ()

    #add_form_template = 'admin/extra/change_form.html'  # then it will use this fle instead of "change_form.html", ModelAdmin : render_change_form
    change_form_template = 'admin/extra/change_form.html'
    change_list_template =  'admin/extra/change_list.html'

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        #js = ['
        #      'inlines%s.js' % extra]        
        js = [
            'js/jquery.min.js',
            'admin/js/jquery.init.both.js',            
            'admin/extra/js/admin/RelatedObjectLookups.js',            
            'admin/extra/js/inlines.js',
        ]
        return super(MyModelAdmin,self).media + forms.Media(js=[static('%s' % url) for url in js])
        
    ##### for LinkForm method#####
    def get_linkform_instances(self, request):
        link_instances = []
        for form_link in self.form_links:
            link_instance = form_link()
            link_instances.append(link_instance)
        return link_instances


    def get_linkform_related_names(self, request):
        related_names = []
        for form_link in self.form_links:
            related_name= None
            if hasattr(form_link, 'related_name'):
                related_name = form_link.related_name
            related_names.append(related_name)
        return related_names

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
        link_init_searchs = []
        for form_link in self.form_links:
            link_init_searchs.append(form_link.link_init_search)
        return link_init_searchs

    def get_linkform_models(self, request):
        link_models = []
        for form_link in self.form_links:
            link_models.append(form_link.link_model)
        return link_models

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

    def _get_related_field_name(self, fk_model, link_model, **kwargs):
        related_field_name = kwargs.get('related_name', None)
        if related_field_name:
            return related_field_name

        link_field_name = None        
        for fieldname in link_model._meta.get_all_field_names():
            field = link_model._meta.get_field(fieldname)
            if hasattr(field, 'related_model'):
                loop_link_model = field.related_model
                if loop_link_model is not None:
                    if loop_link_model.__name__ == fk_model.__name__:
                        link_field_name = fieldname
                        break
        return link_field_name

    def filter_objects(self, fk_model, link_model, fk_obj, **kwargs):
        link_objs = None

        link_field_name = self._get_related_field_name( fk_model, link_model, **kwargs)

        # print ("link_field_name", link_field_name, "fk_obj", fk_obj)
        # print ("fk_model", fk_model, "link_model", link_model)

        if link_field_name:
            link_objs = link_model.objects.filter(**{link_field_name:fk_obj})

        return link_objs

    def get_obj_items(self, instance):
        r_dict = {}
        model = instance.__class__
        for field_name in model._meta.get_all_field_names():
            r_dict.update({field_name:getattr(instance,field_name,None)})
        return r_dict

    def get_linkform_queryset_from_model(self, obj, link_model, **kwargs):

        fk_model = self.model        
        return self.filter_objects(fk_model, link_model, obj, **kwargs)
    
    def get_linkform_formset_initial(self, request, object_id):

        obj = self.get_object(request, unquote(object_id))

        initials = []

        for link_form, related_name, link_model in zip(
                self.get_linkform_forms(request), 
                self.get_linkform_related_names(request), 
                self.get_linkform_models(request)):

            link_objs = self.get_linkform_queryset_from_model(obj, link_model, related_name=related_name)
            initial = [] #list
            if link_objs != None:
                for link_obj in link_objs:
                    form = {} #dict
                    items = self.get_obj_items(link_obj)
                    for field in link_form.base_fields:                 
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
    def _save_obj(self, fk_model, link_obj, link_m2m, obj, **kwargs): # fk_model is self

        link_field_name = self._get_related_field_name(fk_model, link_obj.__class__, **kwargs)
        if link_m2m == False:
            setattr(link_obj, link_field_name, obj)
        else:
            fk_obj =  getattr(link_obj, link_field_name)
            fk_obj.add(obj)      

        '''
        if fk_model == lab_device_item:
            if link_m2m == False:
                link_obj.lab_device_item = obj
            else:
                link_obj.lab_device_item.add(obj)
        '''
            
        link_obj.save()
        
    def _delete_empty_objs(self, fk_model, link_obj, link_m2m, **kwargs):

        if link_m2m == False:
            self.filter_objects(fk_model, link_obj, None, **kwargs).delete()
            print "_delete_empty_objs"
            
            '''
            if fk_model == lab_device_item:                    
                linkobj.objects.filter(lab_device_item= None).delete()
            '''

    '''
    fk_model :  foreignkey or m2m model
    link_m2m : whether this is m2m relationship
    '''
    def _delete_obj(self, fk_model, link_obj, link_m2m, obj, **kwargs):
        related_name = kwargs.get('related_name', None)      


        if link_m2m == True:
            #fk = getattr(link_obj, fk_model._meta.many_to_many)
            if not related_name:
                related_name = fk_model._meta.object_name.lower()        
            # print related_name    
            fk = getattr(link_obj, related_name)
            fk.remove(obj)
            print "_delete_obj"
        else:
            if not related_name:
                related_name = fk_model._meta.object_name + "_id"
            setattr(link_obj, related_name, None)
            link_obj.save()

        '''
        Example:

        if fk_model == lab_device_item:
            if link_m2m == True:
                link_obj.lab_device_item.remove(obj)
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
                for linkobj, link_m2m, related_name in zip(
                        link_models, 
                        self.get_linkform_m2ms(request), 
                        self.get_linkform_related_names(request)):
                    self._delete_empty_objs(self.model, linkobj, link_m2m, related_name=related_name)
                    
            if self.modelform_links != []:
                link_models = []
                for link in self.modelform_links:
                    link_models.append(link.model)
                for linkobj, related_name in zip(link_models, self.get_linkform_related_names(request)):
                    self._delete_empty_objs(self.model, linkobj, False, related_name=related_name)

    
    # should do this in subcass to help extend, write here for simpty !!!
    def _save_link_obj(self, request, obj, link_key = 'id'):
        if self.form_links != []:
            prefixes = {}
            for related_name, link_form, link_model, link_formset, link_m2m in (zip(
                    self.get_linkform_related_names(request),
                    self.get_linkform_forms(request), 
                    self.get_linkform_models(request), 
                    self.get_linkform_formsets(request), 
                    self.get_linkform_m2ms(request))):
                #prefix = LinkObjFormSet.get_default_prefix()
                prefix = link_form.Meta.class_name + "_set"                
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                formset = link_formset(request.POST, request.FILES, prefix = prefix)
                for form in formset.forms:
                    if form.is_valid() and form.cleaned_data.has_key(link_key): 
                        link_obj_id = form.cleaned_data[link_key] #string
                        if link_obj_id.isdigit():
                            link_obj = link_model.objects.get(pk=link_obj_id)                            
                            if formset._should_delete_form(form):
                                self._delete_obj(self.model, link_obj, link_m2m, obj, related_name=related_name)
                                self.log_change(request, obj, '"'+force_text(link_obj)+'"' + ' deleted from  ' + '"' + force_text(obj) + '"')
                            else:
                                self._save_obj(self.model, link_obj, link_m2m, obj, related_name=related_name)
                                self.log_change(request, obj, '"'+force_text(link_obj)+'"' + ' add or modified in  ' + '"' + force_text(obj) + '"')
                                
        if self.modelform_links != []:  #only support ForeignKey inline
            link_instances = self.get_link_instances(request, None)          
            prefixes = {}
            for ifromset, ilink in zip(self.get_link_formsets(request), link_instances): 
                prefix = ifromset.get_default_prefix()   #need to change ??????????/
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = ifromset(data=request.POST, files=request.FILES,
                                  instance=obj,
                                  save_as_new="_saveasnew" in request.POST,
                                  prefix=prefix, queryset=ilink.queryset(request))

                for form in formset.forms:
                    form.is_valid()  # this line is to get cleaned_data, but for modelForm, it's invalid, reason is ObjectExist
                    if form.instance.id != '':
                        link_obj_id = form.instance.id
                        if link_obj_id > 0 : #integer
                            link_obj = ilink.model.objects.get(pk=link_obj_id)                            
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

        # print self.self_form_link
        # print "-------"

        form = self.self_form_link()

        return render_to_response('admin/linked/linkback.html', 
                                            {'array': form.get_back_array(obj), 
                                            'newId' : escape(pk_value), 
                                            'newRepr' : escape(obj),
                                            })

        
    '''
    def save_model(self, request, obj, form, change):
        self.is_add_link_allowed = True
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
        self.is_add_link_allowed = False

        if self.form_links != []:
            prefixes = {}
            for link_instance, link_form, link_m2m, link_initsearch, link_formset in zip(
                    self.get_linkform_instances(request), 
                    self.get_linkform_forms(request), 
                    self.get_linkform_m2ms(request), 
                    self.get_linkform_initsearchs(request), 
                    self.get_linkform_formsets(request)):   
                #prefix = link_formset.get_default_prefix()
                prefix = link_form.Meta.class_name + "_set"
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                if request.method == "POST":                
                    formset = link_formset(request.POST, request.FILES, prefix = prefix)                    
                    if formset.is_valid():
                        formset = self.sort_linkform_formset(request, formset, True)
                        link_admin_obj_formset = LinkFormAdminFormset(formset = formset, link = link_instance)
                    else:
                        link_admin_obj_formset = LinkFormAdminFormset(formset = link_formset(prefix = prefix), link = link_instance)
                else:
                    link_admin_obj_formset = LinkFormAdminFormset(formset = link_formset(prefix = prefix), link = link_instance)
                    
                link_admin_obj_formset.link_m2m = link_m2m
                link_admin_obj_formset.link_init_search = link_initsearch                
                link_admin_obj_formsets.append(link_admin_obj_formset)

            extra_context_cur = {        
                'link_form_admin_formsets':link_admin_obj_formsets,      
                'is_add_link_allowed': self.is_add_link_allowed,
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
                for iformset, ilink in zip(self.get_link_formsets(request), link_instances): 
                    prefix = iformset.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = iformset(data=request.POST, files=request.FILES,
                                      instance=new_object,
                                      save_as_new="_saveasnew" in request.POST,
                                      prefix=prefix, queryset=ilink.queryset(request))
                    formsets.append(formset)
            else:
                prefixes = {}
                for iformset, ilink in zip(self.get_link_formsets(request), link_instances):  
                    prefix = iformset.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = v(instance=self.model(), prefix=prefix,
                                      queryset=ilink.queryset(request))
                    formsets.append(formset)

            link_admin_formsets = []
            link_media = self.media #should implement it for further dev !!!!
            for ilink, iformset in zip(link_instances, formsets):
                fieldsets = list(ilink.get_fieldsets(request))
                readonly = list(ilink.get_readonly_fields(request))
                prepopulated = dict(ilink.get_prepopulated_fields(request))
                link_admin_formset = LinkModelAdminFormSet(ilink, iformset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                link_admin_formset.link_m2m = ilink.link_m2m
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
            self.is_add_link_allowed = False
        else:
            self.is_add_link_allowed = True

        if self.form_links != []:
            initial = self.get_linkform_formset_initial(request,object_id)
            link_admin_obj_formsets = []

            prefixes = {}
            for link_initial, link_instance, link_form, link_formset, link_m2m, link_initsearch in zip(
                    initial, 
                    self.get_linkform_instances(request), 
                    self.get_linkform_forms(request),
                    self.get_linkform_formsets(request), 
                    self.get_linkform_m2ms(request), 
                    self.get_linkform_initsearchs(request)): 
                #prefix = link_formset.get_default_prefix()
                prefix = link_form.Meta.class_name + "_set"                
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])

                if request.method == "POST":                          
                    formset = link_formset(request.POST, request.FILES, prefix = prefix) 
                    if formset.is_valid():
                        formset = self.sort_linkform_formset(request, formset)
                        link_admin_obj_formset = LinkFormAdminFormset(formset = formset, link = link_instance)                    
                    else:
                        link_admin_obj_formset = LinkFormAdminFormset(formset = link_formset(prefix = prefix), link = link_instance)

                else:
                    link_obj_formset = link_formset(initial = link_initial, prefix = prefix)
                    link_admin_obj_formset = LinkFormAdminFormset(formset = link_obj_formset, link = link_instance)
                    
                link_admin_obj_formset.link_m2m = link_m2m
                link_admin_obj_formset.link_init_search = link_initsearch                
                link_admin_obj_formsets.append(link_admin_obj_formset)                
        
            extra_context_cur = {        
                'link_form_admin_formsets':link_admin_obj_formsets,      
                'is_add_link_allowed': self.is_add_link_allowed,
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
                for iformset, ilink in zip(self.get_link_formsets(request, new_object), link_instances):
                    prefix = iformset.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = iformset(request.POST, request.FILES,
                                      instance=new_object, prefix=prefix,
                                      queryset=linkilinkqueryset(request))

                    formsets.append(formset)
                    
                if form_validated:
                    pass
            else:
                prefixes = {}
                for iformset, ilink in zip(self.get_link_formsets(request, obj), link_instances):
                    prefix = iformset.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = iformset(instance=obj, prefix=prefix,
                                      queryset=ilink.queryset(request))
                    formsets.append(formset)

            link_admin_formsets = []
            for ilink, iformset in zip(link_instances, formsets):
                fieldsets = list(ilink.get_fieldsets(request, obj))
                readonly = list(ilink.get_readonly_fields(request, obj))
                prepopulated = dict(ilink.get_prepopulated_fields(request, obj))
                link_admin_formset = LinkModelAdminFormSet(ilink, iformset,
                    fieldsets, prepopulated, readonly, model_admin=self)
                link_admin_formset.link_m2m = ilink.link_m2m                
                link_admin_formset.obj_id = object_id
                link_admin_formsets.append(link_admin_formset)

            context_tmp = {
                'link_admin_formsets': link_admin_formsets,
            }

            if extra_context == None:
                extra_context = {}
            
            extra_context.update(context_tmp or {})

        return super(MyModelAdmin, self).change_view(request,object_id, form_url,extra_context)


class LinkFormAdmin(object):
    """docstring for LinkFormAdmin  similar to InlineAdmin"""
    link_form = None
    link_model = None
    link_m2m = False
    link_init_search = False
    related_name = None
    
    extra = 0
    max_num = None
    can_delete = True
    can_order = True

    template = 'admin/edit_inline/tabular_link.html'
    
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
