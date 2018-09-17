from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
# Create your models here.
from django.db.models.signals import post_delete, post_save, pre_save

from markdown_deux import markdown
from django.utils.safestring import mark_safe

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# def image_upload_to(instance, filename):
#     basename, file_extension = filename.split(".")
#     return "exam/%s" %(basename)

QuestionType = (
    ('choice', 'Choice'),
    ('answer', 'Answer'),

)

CategoryType = (
    ('ip', 'IP'),
    ('linux', 'Linux'),
    ('lte', 'LTE'),
    ('python', 'Python'),
    ('cpp', 'C++'),
    ('robot', 'Robot'),
    ('test', 'Test'),
    ('log', 'LOG'),

)
class ExamLibItem(models.Model):
    title = models.TextField(max_length=500)
    content = models.TextField(max_length=1500, blank=True, null=True)
    type = models.CharField(max_length=45, choices=QuestionType) #Choice
    a = models.TextField(max_length=500, blank=True)
    b = models.TextField(max_length=500, blank=True)
    c = models.TextField(max_length=500, blank=True)
    d = models.TextField(max_length=500, blank=True)
    score = models.PositiveIntegerField(blank=False)
    ref_answer = models.TextField(max_length=500,verbose_name='ref_answer')
    category = models.CharField(max_length=45, choices=CategoryType) #Linux, IP
    source = models.CharField(max_length=120, blank=True, null=True) #EDU, Internet
    contributor = models.CharField(max_length=45, blank=True, null=True) #HE Bin
    # pic = models.ImageField(upload_to=image_upload_to, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self): #Python 3.3 is __str__
        return "%s (%s')" % (self.title, self.score)

    def get_absolute_url_detailview(self):
        try:
            return reverse("examlibitem_detail", kwargs={"pk": self.pk}) #pk for ExamLibItem
        except:
            return '#'
        
    def get_markdown(self):
        content = self.content
        markdown_content = markdown(content, 'recipe')
        return mark_safe(markdown_content)

    def get_markdown_ref_answer(self):
        ref_answer = self.ref_answer
        markdown_content = markdown(ref_answer, 'recipe')
        return mark_safe(markdown_content)

PaperType = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
)

class Paper(models.Model):
    name = models.CharField(verbose_name = "Paper Name", max_length=120) #pre-test    
    type = models.CharField(verbose_name = "Paper Type", max_length=45, choices=PaperType) #A,B    
    examlibitem = models.ManyToManyField(ExamLibItem, verbose_name = "Exam Library Item", blank=True)
    total_score = models.IntegerField()

    def __unicode__(self): 
        return "[%003d] %s" % (self.pk, self.name)

    def get_absolute_url_for_testitem(self):
        return reverse("test_testitem_list", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("paper_examlibitem_list", kwargs={"pk": self.pk})

class ExamItem(models.Model):
    examlibitem = models.ForeignKey(ExamLibItem, null=False, blank=False)    
    paper = models.ForeignKey(Paper, null=False, blank=False)    
    answer = models.TextField(max_length=500, blank=True, default='')    
    # answer = models.TextField(max_length=500,verbose_name='answer')    
    exam_result = models.ForeignKey('ExamResult', null=True, blank=True, default=None)
    score_result = models.PositiveIntegerField(blank=True, default=1)    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __unicode__(self): 
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("examitem_detail", kwargs={"pk": self.pk})

class ExamResult(models.Model):
    paper = models.ForeignKey(Paper, null=False)
    score = models.IntegerField(null=True, blank=True, default =  0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __unicode__(self): 
        return "[examinee] %s - [test] %s - [score] %s" % (self.user, self.paper, self.score)

    def get_absolute_url(self):
        return reverse("examresult_examitem_list", kwargs={"pk": self.pk})

def save_score(sender, instance, **kwargs):
	instance.score = 0
	for _ in instance.examitem_set.all():
		instance.score += _.score_result

pre_save.connect(save_score, sender=ExamResult)

# class Examinee(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

#     def __unicode__(self): 
#         return str(self.pk)