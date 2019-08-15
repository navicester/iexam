from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=45)
    word = models.ManyToManyField('Word', related_name="category", blank=True, null=True)

    def __unicode__(self): 
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=45)
    word = models.ManyToManyField('Word', related_name="tag", blank=True, null=True)

    def __unicode__(self): 
        return self.name

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
    ('other', 'Other'), 
)



# Create your models here.
class Word(models.Model):
    name =  models.CharField(max_length=45, unique=True)
    slug = models.SlugField(max_length=40, blank=True)
    phonetic = models.CharField(max_length=45, null=True, blank=True)
    explain = models.TextField(max_length=300,blank=True, null=True, default = '')
    progress = models.DecimalField(max_digits=50, decimal_places=0, default = 0 )
    in_plan = models.BooleanField(default=False)
    # members = models.ManyToManyField('Word', through='Membership')
    # linked_word = models.ManyToManyField('Word', related_name='related_word',  blank=True)
    linked_word = models.ManyToManyField('Word',  blank=True, null=True)
    etyma_word = models.ManyToManyField('Word', related_name='etyma_word_reverse', blank=True)
    resemblance_word = models.ManyToManyField('Word', related_name='resemblance_word_reverse', blank=True)
    semantic_word = models.ManyToManyField('Word', related_name='semantic_word_reverse', blank=True)
    antonymy_word = models.ManyToManyField('Word', related_name='antonymy_word_reverse', blank=True)    
    book = models.CharField(max_length=120, choices=BOOK_NAME, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = 'name',

    def __unicode__(self): 
        return self.name

    def get_absolute_url(self):
        try:
            # return reverse("word_detail", kwargs={"pk": self.pk})
            return reverse("word_detail", kwargs={"slug": self.slug})
        except:
            return '#'

    def get_next_by_name(self, field='name'):
        field = self.__class__._meta.get_field(field)        
        try:
            return self._get_next_or_previous_by_FIELD(field, is_next=True, in_plan=True, progress__lt=100)
        except Word.DoesNotExist:
            return None

    def get_previous_by_name(self, field='name'):
        field = self.__class__._meta.get_field('name')
        try:
            return self._get_next_or_previous_by_FIELD(field, is_next=False, in_plan=True, progress__lt=100)
        except Word.DoesNotExist:
            return None

def get_related_name_reverse(name):
    name_dict = {
        'etyma' : 'etyma_word',
        'resemblance' : 'resemblance_word',
        'semantic': 'semantic_word',
        'antonymy': 'antonymy_word',

    }
    return name_dict.get(name, None)

# def get_related_word(name):

def save_related_words(instance1, instance2, related_name_reverse):

    if not related_name_reverse:
        return False

    updated = False
    object1_reserve_set = getattr(instance2, related_name_reverse).all()

    # if not (instance1 in object1_reserve_set) and not (instance1 is instance2):
    if not getattr(instance2, related_name_reverse).filter(name=instance1.name) and not (instance1.name == instance2.name):
        print "{} add {}".format(instance2.name, instance1.name)
        updated = True
        getattr(instance2, related_name_reverse).add(instance1) # this will trigger another signal   
    else:
        print "instance2 related set is {}".format(object1_reserve_set)   

    return updated 

def save_words(instance, name):
    
    ever_updated = False
    if hasattr(instance, name):
        wordexp_set = getattr(instance, name).all()
        for _ in wordexp_set:
            word = Word.objects.filter(name=_.name).first()
            if word:
                related_name_reverse = get_related_name_reverse(name)
                if related_name_reverse:
                    saved = [False, False]
                    saved[0] = save_related_words(instance, word, related_name_reverse)
                    saved[1] = save_related_words(word,instance, related_name_reverse)
                    if saved[0] or saved[1]:
                        ever_updated = True
                        word.save()

                # if not (instance in word.linked_word.all()) and not (instance is word):
                #     print ">>>>>>> {} add {}".format(word.name, instance.name)
                #     updated[0] = True
                #     ever_updated = True
                #     word.linked_word.add(instance) # this will trigger another signal   
                # else:
                #     print "a ha 1, word.linked_word.all is {}".format(word.linked_word.all())
                updated = [False, False]
                updated[0] = save_related_words(instance, word, 'linked_word')


                # this doesn't work? add m2m_changed to complete this reverse action
                # if not (word in instance.linked_word.all()) and not (instance is word):
                #     print "<<<<<<<< {} add {}".format(instance.name, word.name)
                #     updated[1] = True
                #     instance.linked_word.add(word)
                #     ever_updated = True                      
                # else:
                #     print "a ha 2, instance.linked_word.all is {}".format(instance.linked_word.all())
                updated[1] = save_related_words(word, instance, 'linked_word')

                if updated[0] or updated[1]:
                    ever_updated = True
                    word.save()

    if ever_updated:
        instance.save()


def words_changed1(sender, instance, **kwargs):
    # print "Enter words_changed1"
    instance.slug = slugify(instance.name)
    
    if instance:
        save_words(instance, 'wordexp')        
        save_words(instance, 'etyma')
        save_words(instance, 'resemblance')
        save_words(instance, 'semantic')
        save_words(instance, 'antonymy')
    else:
        print "instance is null"

    # print "Exit words_changed1"

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

class WordExpQuerySet(models.query.QuerySet):
    def notempty(self):
        # HOW to exclude \r\n? why sentence__isnull=True not work?
        sentences = [_.sentence for _ in self.exclude(sentence__isnull=True) if _.sentence]

        return self.filter(sentence__in=sentences)
        # return self.filter(sentence__isnull=False).distinct()
        # return self.filter(sentence__icontains=' ')
        # return self.exclude(sentence__startswith='')

class WordExpManager(models.Manager):
    def get_queryset(self):
        return WordExpQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().notempty()
        # return super(WordExpManager, self).filter(sentence__isnull=False)

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

    objects = WordExpManager()

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
    book = models.CharField(max_length=120, choices=DICT, default='youdao')

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

