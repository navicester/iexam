
from django import forms
from django.forms.models import ModelForm

from .models import *

class WordExpForm(ModelForm):
    class Meta:
        model = WordExp
        verbose_name = 'Word Exp'
        
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
        super(WordExpForm, self).__init__(*args, **kwargs)
        self.fields['id'].label = "id"
        self.fields['phonetic'].label = "phonetic"
        self.fields['explain'].label = "explain"
        self.fields['sentence'].label = "sentence"        
    '''
