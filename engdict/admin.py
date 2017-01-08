from django.contrib import admin

# Register your models here.
from .models import *

from .helpers_linkform import LinkFormAdmin
from .link_forms import *
from .options import MyModelAdmin

from django.contrib.admin.options import *
csrf_protect_m = method_decorator(csrf_protect)

class WordExpLinkFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = WordExpForm
    link_obj_class = WordExp
    link_m2m = True
    link_init_search = True

class ExampleWordInline(admin.TabularInline):
    model = ExampleWord
    extra = 0

class WordDictInline(admin.TabularInline):
    model = WordDict
    extra = 0

class WordExpAdmin(MyModelAdmin):
    list_display = ['phonetic','explain', 'sentence']
    self_form_link = WordExpForm
    
    class Meta:
        model = WordExp

class WordAdmin(MyModelAdmin):
    list_display = ['name','phonetic', 'progress']
    inlines = [
        # ExampleWordInline,
        # WordDictInline,
    ]

    form_links = [WordExpLinkFormAdmin]

    class Meta:
        model = Word

    @csrf_protect_m
    #@transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}        
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)
        
        return super(WordAdmin, self).add_view(request,form_url,extra_context)

    # @csrf_protect_m
    # #@transaction.commit_on_success
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = {}        
    #     extra_context_cur = {
    #     }

    #     extra_context.update(extra_context_cur)

    #     return super(WordAdmin, self).change_view(request,object_id, form_url,extra_context)

class MembershipAdmin(admin.ModelAdmin):
    list_display = ['word','exampleWord', 'relation']
    class Meta:
        model = Membership

admin.site.register(Word, WordAdmin)
admin.site.register(WordExp, WordExpAdmin)
admin.site.register(Membership, MembershipAdmin)