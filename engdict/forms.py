from django import forms
from django.utils.html import escape, escapejs

from adminextend.forms import LinkFormAdminForm

from django.forms.models import ModelForm
from .models import *

class WordExpForm(LinkFormAdminForm):
    class Meta:
        verbose_name = 'Word Exp'
        class_name = "WordExp"

        back_field = [
            "name",
            "phonetic",
            "explain",
            "sentence",
            "book"]
        
    # these declared are base field
        
    id = forms.CharField(max_length=11, label = "id", widget = forms.TextInput(attrs={'readonly':'readonly','disable':True, 'hidden':False})) 
    name = forms.CharField(max_length=11, label = "name", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    
    phonetic = forms.CharField(max_length=11, label = "phonetic", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    explain = forms.CharField(max_length=50, label = "explain", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    sentence = forms.CharField(max_length=11, label = "sentence", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))  
    book = forms.CharField(max_length=11, label = "book", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))      

    def __unicode__(self):
        return u'%s %s' % (self.id, self.explain)  

    def is_valid(self):
        return super(WordExpForm, self).is_valid()            

'''
    def get_back_array(self, obj):
        array= []
        array.append("phonetic")
        array.append(escape(obj.phonetic))
        array.append("explain")
        array.append(escape(obj.explain))
        array.append("sentence")
        array.append(escape(obj.sentence.replace('\r\n',"brbr")))        
        array.append("book")
        array.append(escape(obj.book))

        return array
'''


class WordExpModelForm(ModelForm):
    class Meta:
        model = WordExp
        verbose_name = 'Word Exp'

        exclude = []
        
    id = forms.CharField(max_length=11, widget = forms.TextInput(attrs={'readonly':'readonly','disable':True}), label = 'id') 
    phonetic = forms.CharField(max_length=11, required=False, label = 'Name', widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    explain = forms.CharField(max_length=50, label = 'explain', required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    sentence = forms.CharField(max_length=11, label = 'sentence', required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    book = forms.CharField(max_length=11, label = 'book', required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))   
    def __unicode__(self):
        return u'%s %s' % (self.id, self.explain)  

    ''' # why here it doesn't work ?
    def __init__(self, *args, **kwargs):
        super(WordExpModelForm, self).__init__(*args, **kwargs)
        self.fields['id'].label = "id"
        self.fields['phonetic'].label = "phonetic"
        self.fields['explain'].label = "explain"
        self.fields['sentence'].label = "sentence"        
    '''

class WordDictForm(LinkFormAdminForm):
    class Meta:
        verbose_name = 'Word Dict'
        class_name = "WordDict"

        back_field = [
            "explain",
            "book"]
        
    # these declared are base field
        
    id = forms.CharField(max_length=11, label = "id", widget = forms.TextInput(attrs={'readonly':'readonly','disable':True, 'hidden':False})) 
    explain = forms.CharField(max_length=50, label = "explain", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))    
    book = forms.CharField(max_length=11, label = "book", required=False, widget = 
                             forms.TextInput(attrs={'readonly':'readonly','disable':True}))      

    def __unicode__(self):
        return u'%s %s' % (self.id, self.explain)  

    def is_valid(self):
        return super(WordDictForm, self).is_valid()           
