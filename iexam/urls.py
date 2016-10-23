from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from exam.views import (TestItemList,                 
                examhome,ExamItemList, ExamItemDetail,
                PaperList,ExamLibItemList, ExamLibItemDetail,
                )

urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),   
    url(r'^about/$', 'iexam.views.about', name='about'),

    # test
    url(r'^testhome/$', 'exam.views.testhome', name='testhome'),
    url(r'^test/(?P<pk>\d+)/$', TestItemList.as_view(), name='test_testitem_list'),

    # paper
    url(r'^paper/$', PaperList.as_view(), name='paper'),
    url(r'^paper/(?P<pk>\d+)/$', ExamLibItemList.as_view(), name='paper_examlibitem_list'),
    url(r'^paper/examlibitem/(?P<pk>\d+)/$', ExamLibItemDetail.as_view(), name='examlibitem_detail'),

    # exam
    url(r'^examhome/$', 'exam.views.examhome', name='examhome'),
    url(r'^examresult/(?P<pk>\d+)/$', ExamItemList.as_view(), name='examresult_examitem_list'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.backends.default.urls')),    
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
