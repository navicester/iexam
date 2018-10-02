from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
    name = models.CharField(max_length=45)
    word = models.ManyToManyField('Word', blank=True, null=True)

    def __unicode__(self): 
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=45)
    word = models.ManyToManyField('Word', blank=True, null=True)

    def __unicode__(self): 
        return self.name

# Create your models here.
class Word(models.Model):
    name =  models.CharField(max_length=45)
    phonetic = models.CharField(max_length=45, null=True, blank=True)
    explain = models.TextField(max_length=120,blank=True, null=True, default = '')
    progress = models.DecimalField(max_digits=50, decimal_places=0, default = 0 )
    in_plan = models.BooleanField(default=False)
    # members = models.ManyToManyField('Word', through='Membership')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = 'name',

    def __unicode__(self): 
        return self.name

    def get_absolute_url(self):
        try:
            return reverse("word_detail", kwargs={"pk": self.pk})
        except:
            return '#'

    def get_next_by_name(self):
        field = self.__class__._meta.get_field('name')
        return self._get_next_or_previous_by_FIELD(field, is_next=True)
        try:
            return self._get_next_or_previous_by_FIELD('name', is_next=True)
        except Word.DoesNotExist:
            return None

    def get_previous_by_name(self):
        field = self.__class__._meta.get_field('name')
        return self._get_next_or_previous_by_FIELD(field, is_next=False)
        return self._get_next_or_previous_by_FIELD('name', is_next=False)
        try:
            return self._get_next_or_previous_by_FIELD('name', is_next=False)
        except Word.DoesNotExist:
            return None

BOOK_NAME = (
    ('nce3', 'NCE3'),
    ('nce4', 'NCE4'),
    ('bbc', 'BBC'),
    ('voa', 'VOA'),
    ('cctvnews', 'CCTVNEWS'),
    ('mail', 'MAIL'),
    ('life', 'LIFE'),
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
    phonetic = models.CharField(max_length=45, null=True, blank=True)
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

