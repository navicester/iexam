from django.contrib import admin
from django.http import HttpResponse
import csv
import codecs
# Register your models here.
from .models import *

from .forms import *

from adminextend.options import MyModelAdmin, LinkFormAdmin

from django.contrib.admin.options import *
csrf_protect_m = method_decorator(csrf_protect)

class WordDictInline(admin.TabularInline):
    model = WordDict
    extra = 0
    # max_num = 1

class WordDictLinkFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = WordDictForm
    link_model = WordDict
    link_m2m = False
    link_init_search = True

class WordLinkFormAdmin(LinkFormAdmin):

    extra = 1
    
    link_form = WordForm
    link_model = Word
    link_m2m = True
    link_init_search = True

    related_name= 'linked_word' # 'related_word'

class WordLinkEtymaFormAdmin(WordLinkFormAdmin):

    related_name= 'etyma_word'
    link_form = WordEtymaForm

class WordLinkResemblanceFormAdmin(WordLinkFormAdmin):

    related_name= 'resemblance_word'
    link_form = WordResemblanceForm

class WordLinkSemanticFormAdmin(WordLinkFormAdmin):

    related_name= 'semantic_word'
    link_form = WordSemanticForm

class WordLinkAntonymyFormAdmin(WordLinkFormAdmin):

    related_name= 'antonymy_word'
    link_form = WordAntonymyForm
            
class WordLinkForCategoryFormAdmin(LinkFormAdmin):

    extra = 1
    
    link_form = WordForm
    link_model = Word
    link_m2m = True
    link_init_search = True

    related_name= 'category'

class WordLinkForTagFormAdmin(LinkFormAdmin):

    extra = 1
    
    link_form = WordForm
    link_model = Word
    link_m2m = True
    link_init_search = True

    related_name= 'tag'

class WordExpLinkFormAdmin(LinkFormAdmin):

    extra = 1
    
    link_form = WordExpForm
    link_model = WordExp
    link_m2m = True
    link_init_search = True

    related_name='word' # if have severl same m2m, related_name must be specified, otherwise _get_related_field_name will fail



class WordExpEtymaLinkFormAdmin(WordExpLinkFormAdmin):
    related_name = 'etyma'
    link_form = WordExpEtymaForm

class WordExpResemblanceLinkFormAdmin(WordExpLinkFormAdmin):
    related_name = 'resemblance'
    link_form = WordExpResemblanceForm

class WordExpSemanticLinkFormAdmin(WordExpLinkFormAdmin):
    related_name = 'semantic'
    link_form = WordExpSemanticForm

class WordExpAntonymyLinkFormAdmin(WordExpLinkFormAdmin):
    related_name = 'antonymy'
    link_form = WordExpAntonymyForm

class WordExpRelatedLinkFormAdmin(WordExpLinkFormAdmin):
    related_name = 'related'
    link_form = WordExpRelatedForm

class CategoryLinkFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = CategoryForm
    link_model = Category
    link_m2m = True
    link_init_search = True

class TagLinkFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = TagForm
    link_model = Tag
    link_m2m = True
    link_init_search = True

class WordDictFormAdmin(LinkFormAdmin):

    extra = 0
    
    link_form = WordDictForm
    link_model = WordDict
    link_m2m = False
    link_init_search = True

class CategoryAdmin(MyModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]
    ordering = ['name',]

    # filter_horizontal = ['word']

    self_form_link = CategoryForm

    form_links = [ 
        WordLinkForCategoryFormAdmin,
    ]

    class Meta:
        model = Category

    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)
        
        return super(CategoryAdmin, self).add_view(request,form_url,extra_context)

    @csrf_protect_m
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)

        return super(CategoryAdmin, self).change_view(request,object_id, form_url,extra_context)


class TagAdmin(MyModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]
    ordering = ['name',]

    # filter_horizontal = ['word']

    self_form_link = TagForm

    form_links = [ 
        WordLinkForTagFormAdmin,
    ]

    class Meta:    
        model = Tag

    # app_name will be used to get HREF of search or add
    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)
        
        return super(TagAdmin, self).add_view(request,form_url,extra_context)

    @csrf_protect_m
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'app_name': 'engdict'}     
        extra_context_cur = {
        }

        extra_context.update(extra_context_cur)

        return super(TagAdmin, self).change_view(request,object_id, form_url,extra_context)


class WordExpAdmin(MyModelAdmin):
    list_display = ['name','phonetic','explain', 'sentence', 'book']
    search_fields = ['name','phonetic','explain', 'sentence',]
    ordering = ['name','book','relation', 'etymon']
    list_filter = ('book','relation', 'etymon')
    # filter_horizontal = ['word']
    list_editable  = ['explain']
    list_per_page = 20

    self_form_link = WordExpForm

    fieldsets= (
        (None,{
            'classes': ('filedset-left',),
            'fields':
                (
                 'name',
                 'phonetic',
                 'explain',
                 'sentence',
                 'book',
                 'word',
                 )}),
        (None,{
            'classes': ('filedset-right collapse0',),
            'fields':
                (
                 'relation',
                 'etymon',
                 )}),        
        )

    # readonly_fields= (
    #              'name',
    #              ) 

    # fieldsets_fk= (None,{
    #          'fields':
    #             (
    #              'word',
    #              )})

    class Meta:
        model = WordExp

class WordAdmin(MyModelAdmin):
    list_display = [
        'name',
        'phonetic', 
        'book',
        'explain',
        'in_plan', 
        'is_favorite',
        'progress',
        'timestamp', 
        'updated'
    ]

    search_fields = ['name','phonetic' ,'explain']
    ordering = ['name',]
    list_filter = ('in_plan', 'is_favorite','book', 'progress')
    list_editable  = [
        'in_plan', 
        'is_favorite',
        'progress',
        'book',
        # 'explain',        
        ]


    # time consuming

    # fieldsets= (
    #     (None,{
    #         'classes': ('filedset-left',),
    #         'fields':
    #             (
    #             'name',
    #             'phonetic', 
    #             'book',
    #             'explain',
    #             'in_plan', 
    #             'progress',
    #              )}),
    #     ('M2M',{
    #         # 'classes': ('filedset-right collapse0',),
    #         'fields':
    #             (
    #               # 'linked_word',
    #             'etyma_word',                                   
    #             'resemblance_word', # shape or phonetic
    #             'semantic_word', # 
    #             # 'antonymy_word',
    #              )}),        
    #     )

    # filter_horizontal = [
    #     'linked_word',
    #     'etyma_word',   
    #     'resemblance_word',
    #     'semantic_word',
    #     'antonymy_word',
    # ]
    
    inlines = [
        WordDictInline,
    ]

    actions = ['export_selected', 'export_all_favorite', ]    

    self_form_link = WordForm

    form = WordAdminForm # comments this if you want to use fieldsets

    form_links = [ 

        WordExpLinkFormAdmin,
        # use Word M2M directly
        # WordExpEtymaLinkFormAdmin,
        # WordExpResemblanceLinkFormAdmin,
        # WordExpSemanticLinkFormAdmin,
        # WordExpAntonymyLinkFormAdmin,
        WordExpRelatedLinkFormAdmin,

        # WordLinkFormAdmin,
        # below 4 will be automatically updated if change relevant word exp, comment them to use buit-in m2m instead
        WordLinkEtymaFormAdmin,
        WordLinkResemblanceFormAdmin,
        WordLinkSemanticFormAdmin,
        # WordLinkAntonymyFormAdmin,

        # CategoryLinkFormAdmin,
        # TagLinkFormAdmin,

        # WordDictLinkFormAdmin
    ]

    class Meta:
        model = Word

    # class Media:
    #     css = {
    #         "all": ("css/model_admin.css","css/word.css")
    #     }
    #     js = ("js/jquery.min.js","js/model_admin.js",)


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


    def export_selected(self, request, queryset):
        print queryset
        qs = queryset
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="words.csv"'
        response.write(codecs.BOM_UTF8) # add bom header
        writer = csv.writer(response)

        
        writer.writerow(['id', 'name','phonetic','explain', 'progress', 'in_plan', 'is_favorite','book','sentence'])
        for obj in qs:
            row = []
            row.append(obj.pk)
            row.append(obj.name)
            row.append(obj.phonetic)
            row.append(obj.explain)
            row.append(obj.progress)
            row.append(obj.in_plan)
            row.append(obj.is_favorite)
            row.append(obj.book)
            sentences = []          
            for _ in obj.wordexp.all():
                if _.sentence:
                    if not _.sentence in sentences:
                        sentences.append(_.sentence)
            for _ in obj.related.all():
                if _.sentence:
                    if not _.sentence in sentences:
                        sentences.append(_.sentence)
            for etyma in  obj.etyma_word.all():
                for _ in etyma.wordexp.all():
                    if _.sentence:
                        if not _.sentence in sentences:
                            sentences.append(_.sentence)
            for resemblance in  obj.resemblance_word.all():
                for _ in resemblance.wordexp.all():
                    if _.sentence:
                        if not _.sentence in sentences:
                            sentences.append(_.sentence)
            for semantic in  obj.semantic_word.all():
                for _ in semantic.wordexp.all():
                    if _.sentence:
                        if not _.sentence in sentences:
                            sentences.append(_.sentence)
            for antonymy in  obj.antonymy_word.all():
                for _ in antonymy.wordexp.all():
                    if _.sentence:
                        if not _.sentence in sentences:
                            sentences.append(_.sentence)
            # for linked in  obj.linked_word.all():
            #     for _ in linked.wordexp.all():
            #         if _.sentence:
            #             if not _.sentence in sentences:
            #                 sentences.append(_.sentence)
            sentence = "\r\n".join(sentences)
            row.append(sentence)
            writer.writerow(row)    


        return response

    def export_all_favorite(self, request, queryset):
        return self.export_selected(request, Word.objects.filter(is_favorite=True))

class WordDictAdmin(admin.ModelAdmin):
    list_display = ['word','book']
    search_fields = ['word','explain','book']
    ordering = ['book',]
    list_filter = ('book',)
    raw_id_fields = ['word']


class ExampleWordInline(admin.TabularInline):
    model = ExampleWord
    extra = 0

class MembershipAdmin(admin.ModelAdmin):
    list_display = ['word','exampleWord', 'relation']
    class Meta:
        model = Membership

admin.site.register(Word, WordAdmin)
admin.site.register(WordExp, WordExpAdmin)
admin.site.register(WordDict, WordDictAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Membership, MembershipAdmin)
