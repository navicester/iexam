from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Word(models.Model):
    name =  models.CharField(max_length=45)
    phonetic = models.CharField(max_length=45)
    explain = models.TextField(max_length=120,blank=True, null=True, default = '')
    progress = models.DecimalField(max_digits=50, decimal_places=0, default = 0 )
    # members = models.ManyToManyField('Word', through='Membership')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self): 
        return self.name

    def get_absolute_url(self):
        try:
            return reverse("word_detail", kwargs={"pk": self.pk})
        except:
            return '#'

BOOK_NAME = (
    ('nce3', 'NCE3'),
    ('nce4', 'NCE4'),
    ('bbc', 'BBC'),
    ('voa', 'VOA'),
    ('cctvnews', 'CCTVNEWS'),
    ('mail', 'MAIL'),
    ('20000', '20000'),
    ('22000', '22000'),
    ('100days', '100days'),
    ('IELTS', 'IELTS'),
    ('BSWX', 'BSWX'),
    ('YOUDAO', 'YOUDAO'),
)

RELATION = (
    ('Self', 'Self'),
    ('synonym', 'Synonym'),
    ('antonym', 'Antonym'),
    ('homograph', 'Homograph'),
    ('etymon', 'etymon'),
)


class WordExp(models.Model):
    name =  models.CharField(max_length=45)
    phonetic = models.CharField(max_length=45)
    explain = models.CharField(max_length=120, default = '')
    sentence = models.TextField(blank=True, null=True)
    book = models.CharField(max_length=120, choices=BOOK_NAME)
    word = models.ManyToManyField(Word, blank=True)
    relation = models.CharField(max_length=120, default='Self', choices=RELATION)
    etymon = models.CharField(max_length=45, null=True, blank=True)

    def __unicode__(self): 
        return self.explain

DICT = (
    ('youdao', 'YOUDAO'),
    ('kingsoft', 'kingsoft'),
)
class WordDict(models.Model):
    word =  models.ForeignKey(Word)
    explain = models.TextField(blank=True, null=True)
    book = models.CharField(max_length=120, choices=DICT)

    def __unicode__(self): 
        return self.word.name



class ExampleWord(models.Model):
    word =  models.ForeignKey(Word)
    explain = models.CharField(max_length=120, default = '')
    sentence = models.TextField(blank=True, null=True)
    book = models.CharField(max_length=120, choices=BOOK_NAME)

    def __unicode__(self): 
        return self.word.name
        
class Membership(models.Model):
    word = models.ForeignKey(Word)
    exampleWord = models.ForeignKey(ExampleWord)
    etymon = models.CharField(max_length=45)
    relation = models.CharField(max_length=120, choices=RELATION)

    def __unicode__(self):
        return self.word_primary + self.word_secondary

