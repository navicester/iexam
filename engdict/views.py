from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from  django.views.generic.list import ListView

# Create your views here.
from plugin.mixins import (
    TableListViewMixin,
    TableDetailViewMixin,
    UpdateViewMixin,
    CreateViewMixin,
    DeleteViewMixin,
    PaginationMixin,
    StaffRequiredMixin,
    SuperRequiredMixin,
    LoginRequiredMixin
    )
from .models import *

class WordListView(TableListViewMixin, ListView):
    model = Word

    fields_exclude = [
        'in_plan',
        'timestamp',
        'updated',
        ]

    def get_queryset(self, *args, **kwargs):
        qs = super(WordListView, self).get_queryset().filter(in_plan=True, progress__lt=100)
        order = self.request.GET.get('order', None)

        if order and 'latest' == order:
            qs = qs.order_by('-updated')
        return qs

    # fields = [
    #     'name',
    #     'phonetic',
    #     'explain',
    #     'progress',
    #     'updated'
    # ]

class WordDetailView(TableDetailViewMixin, DetailView):
    model = Word
    template_name = "word_detail.html"

    # fields = [
    #     'name',
    #     'phonetic',
    #     'explain',
    #     'progress',
    #     'updated'
    # ]  

    fields_exclude = [
        'slug',
        'in_plan',
        'timestamp',
        'updated',
        'linked_word',
        'etyma_word',
        'resemblance_word',
        'semantic_word',
        'antonymy_word',
        'progress'
    ]    

    def previous(self, *args, **kwargs):
        obj = self.get_object()
        order = self.request.GET.get('order', None)
        order = "latest" # use session to store later
        if order and order == "latest":
            field = "updated"
            return obj.get_next_by_name(field=field, **kwargs)  
        else:
            field = "name"
            return obj.get_previous_by_name(field=field, **kwargs)  

    def next(self, *args, **kwargs):
        obj = self.get_object()
        order = self.request.GET.get('order', None)
        order = "latest" # use session to store later
        if order and order == "latest":
            field = "updated"
            return obj.get_previous_by_name(field=field, **kwargs)  
        else:
            field = "name"     
            return obj.get_next_by_name(field=field, **kwargs)     
        

    def get_context_data(self, *args, **kwargs):
        context = super(WordDetailView, self).get_context_data(*args, **kwargs)

        fields_worddict_name = [
            'explain',
            'book'
            ]
        context["fields_worddict"] = [_ for _ in WordDict._meta.get_fields() if _.name in fields_worddict_name ]
        context["fields_worddict_name"] = fields_worddict_name

        # fields_wordexp_name = [
        #     'name',
        #     'phonetic',
        #     'explain',
        #     'sentence', 
        #     'book', 
        #     # 'relation', 
        #     # 'etymon'
        #     ]
        # context["fields_wordexp"] = [_ for _ in WordExp._meta.get_fields() if _.name in fields_wordexp_name]
        # context["fields_wordexp_name"] = fields_wordexp_name

        fields_wordexp_related_name = [
            # 'name',
            'phonetic',
            'explain',
            'sentence', 
            'book', 
            # 'relation', 
            # 'etymon'
            ]
        context["fields_wordexp_related"] = [_ for _ in WordExp._meta.get_fields() if _.name in fields_wordexp_related_name]
        context["fields_wordexp_related_name"] = fields_wordexp_related_name

        fields_word_name = [
            'name',
            'phonetic',
            'explain',
            # 'sentence', 
            'book', 
            # 'relation', 
            # 'etymon'
            ]
        context["fields_word"] = [_ for _ in Word._meta.get_fields() if _.name in fields_word_name]
        context["fields_word_name"] = fields_word_name

        context["fields_lb_content"] = ['explain', 'sentence']

        obj = self.get_object()
        related_word_exp_lst = []
        for related_word in obj.linked_word.all():  # only get linked_word, may extend to etyma_word ... if needed
            for related_word_exp in related_word.wordexp.all():
                if ((not related_word_exp in obj.etyma.all()) and 
                   (not related_word_exp in obj.resemblance.all()) and 
                   (not related_word_exp in obj.semantic.all()) and 
                   (not related_word_exp in obj.antonymy.all()) and 
                   (not related_word_exp in obj.related.all()) and 
                   (not related_word_exp in obj.wordexp.all()) and 
                   (not related_word_exp in related_word_exp_lst)):
                    if related_word_exp.sentence:
                        related_word_exp_lst.append(related_word_exp)
        context["related_word_exp_lst"] = related_word_exp_lst

        param = {'in_plan':True, 'progress__lt':100}
        context["previous"] = self.previous(**param)
        context["next"] = self.next(**param)

        return context
    