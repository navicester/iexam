from django.conf.urls import include, url

from .views import *

urlpatterns = [
    # test operation
#     url(r'^testhome/$', 'exam.views.testhome', name='testhome'),
    
#     url(r'^test/(?P<pk>\d+)/$', TestItemList.as_view(), name='test_testitem_list'),

#     # paper lib
#     url(r'^paper/$', PaperList.as_view(), name='paper'),
#     url(r'^paper/(?P<pk>\d+)/$', PaperDetailView.as_view(), name='paper_examlibitem_list'),
#     url(r'^paper/examlibitem/(?P<pk>\d+)/$', ExamLibItemUpdateView.as_view(), name='examlibitem_detail'),

#     # exam result
#     url(r'^examhome/$', 'exam.views.examhome', name='examhome'),
#     url(r'^examresult/(?P<pk>\d+)/$', ExamResultDetailView.as_view(), name='examresult_examitem_list'),
#     url(r'^examresult/examitem/(?P<pk>\d+)/$', ExamItemDetail.as_view(), name='examitem_detail'),
]

