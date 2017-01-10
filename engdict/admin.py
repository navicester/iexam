from django.contrib import admin

# Register your models here.
from .models import *

from .helpers_linkform import LinkFormAdmin
from .link_forms import *
from .options import MyModelAdmin

from django.contrib.admin.options import *
csrf_protect_m = method_decorator(csrf_protect)

class WordDictInline(admin.TabularInline):
    model = WordDict
    extra = 0


class WordExpLinkFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = WordExpForm
    link_obj_class = WordExp
    link_m2m = True
    link_init_search = True

class WordExpAdmin(MyModelAdmin):
    list_display = ['name','phonetic','explain', 'sentence']
    search_fields = ['name','phonetic','explain', 'sentence']
    ordering = ['name','book','relation', 'etymon']
    list_filter = ('name','book','relation', 'etymon')
    self_form_link = WordExpForm

    fieldsets= [
        (None,{
             'fields':
                (
                 'name',
                 'phonetic',
                 'explain',
                 'sentence',
                 'book',
                 # 'word',
                 'relation',
                 'etymon',
                 )}),
        ]    

    readonly_fields= (
                 'name',
                 ) 

    # fieldsets_fk= (None,{
    #          'fields':
    #             (
    #              'word',
    #              )})

    class Meta:
        model = WordExp

class WordAdmin(MyModelAdmin):
    list_display = ['name','phonetic', 'progress']
    inlines = [
        WordDictInline,
    ]

    form_links = [WordExpLinkFormAdmin]

    class Meta:
        model = Word

    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)
        
        return super(WordAdmin, self).add_view(request,form_url,extra_context)

    @csrf_protect_m
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)

        return super(WordAdmin, self).change_view(request,object_id, form_url,extra_context)

class ExampleWordInline(admin.TabularInline):
    model = ExampleWord
    extra = 0

class MembershipAdmin(admin.ModelAdmin):
    list_display = ['word','exampleWord', 'relation']
    class Meta:
        model = Membership

admin.site.register(Word, WordAdmin)
admin.site.register(WordExp, WordExpAdmin)
# admin.site.register(Membership, MembershipAdmin)