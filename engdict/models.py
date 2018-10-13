from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save, m2m_changed

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
    # linked_word = models.ManyToManyField('Word', related_name='related_word',  blank=True)
    linked_word = models.ManyToManyField('Word',  blank=True)
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
        try:
            return self._get_next_or_previous_by_FIELD(field, is_next=True, in_plan=True)
        except Word.DoesNotExist:
            return None

    def get_previous_by_name(self):
        field = self.__class__._meta.get_field('name')
        try:
            return self._get_next_or_previous_by_FIELD(field, is_next=False, in_plan=True)
        except Word.DoesNotExist:
            return None


def save_words(instance, name):
    updated = [False, False]
    ever_updated = False
    word_set = getattr(instance, name).all()
    for _ in word_set:
        word = Word.objects.filter(name=_.name).first()
        if word:
            if not (instance in word.linked_word.all()) and not (instance is word):
                print ">>>>>>> {} add {}".format(word.name, instance.name)
                updated[0] = True
                ever_updated = True
                word.linked_word.add(instance) # this will trigger another signal   
            else:
                print "a ha 1, word.linked_word.all is {}".format(word.linked_word.all())

            # this doesn't work? add m2m_changed to complete this reverse action
            if not (word in instance.linked_word.all()) and not (instance is word):
                print "<<<<<<<< {} add {}".format(instance.name, word.name)
                updated[1] = True
                instance.linked_word.add(word)
                ever_updated = True                      
            else:
                print "a ha 2, instance.linked_word.all is {}".format(instance.linked_word.all())

        if word and updated[0] or updated[1]:
            print "^^^^^^ before save word"
            word.save()
            print "^^^^^^ end save word" 

    # if ever_updated:
    #     print "^^^^^^ before save instance"
    #     instance.save()
    #     print "^^^^^^ before save instance"

def words_changed1(sender, instance, **kwargs):
    print "Enter words_changed1"
    
    if instance:
        save_words(instance, 'etyma')
        save_words(instance, 'resemblance')
        save_words(instance, 'semantic')
        save_words(instance, 'antonymy')
        save_words(instance, 'wordexp')
    else:
        print "instance is null"

    print "Exit words_changed1"

pre_save.connect(words_changed1, sender=Word)

def toppings_changed2(sender, instance, **kwargs):
    # be carefule, this can introduce reclusively calling if not process properly
    for _ in instance.linked_word.all():
        if not (instance in _.linked_word.all()) and not (_ is instance):
            _.linked_word.add(instance)
            _.save()
        if not (_ in instance.linked_word.all())  and not (_ is instance):
            instance.linked_word.add(_)
            instance.save()

m2m_changed.connect(toppings_changed2, sender=Word.linked_word.through)

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

def toppings_changed(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance:
        name = instance.name
        try:
            word = Word.objects.filter(name=instance.name).first()
            instance.etyma.add(word)
        except:
            pass

class WordExp(models.Model):
    name =  models.CharField(max_length=45)
    phonetic = models.CharField(max_length=45, null=True, blank=True)
    explain = models.CharField(max_length=120, default = '')
    sentence = models.TextField(blank=True, null=True)
    book = models.CharField(max_length=120, choices=BOOK_NAME)
    etyma = models.ManyToManyField(Word, related_name='etyma', blank=True)
    resemblance = models.ManyToManyField(Word, related_name='resemblance', blank=True)
    semantic = models.ManyToManyField(Word, related_name='semantic', blank=True)
    antonymy = models.ManyToManyField(Word, related_name='antonymy', blank=True)
    related = models.ManyToManyField(Word, related_name='related', blank=True)
    word = models.ManyToManyField(Word, related_name='wordexp', blank=True)
    relation = models.CharField(max_length=120, default='Self', choices=RELATION)
    etymon = models.CharField(max_length=45, null=True, blank=True)

    def __unicode__(self): 
        return self.explain

    @property
    def exp(self):
        return "{} {}".format(self.name, self.explain)

# m2m_changed.connect(toppings_changed, sender=WordExp.etyma.through)

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

