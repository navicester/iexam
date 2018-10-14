from django.conf.urls import include, url

from .views import *

urlpatterns = [

    url(r'^$', WordListView.as_view(), name='words'),
    # url(r'^(?P<pk>\d+)/$', WordDetailView.as_view(), name='word_detail'),
    url(r'^(?P<slug>[\w-]+)/$', WordDetailView.as_view(), name='word_detail'),
]

