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

    def get_context_data(self, *args, **kwargs):
        context = super(WordDetailView, self).get_context_data(*args, **kwargs)
        fields_worddict_name = [
            'explain',
            # 'book'
            ]
        context["fields_worddict"] = [_ for _ in WordDict._meta.get_fields() if _.name in fields_worddict_name ]
        fields_wordexp_name = [
            'explain',
            'sentence', 
            # 'book', 
            'relation', 
            'etymon'
            ]
        context["fields_wordexp"] = [_ for _ in WordExp._meta.get_fields() if _.name in fields_wordexp_name]
        print context["fields_worddict"]
        return context
    