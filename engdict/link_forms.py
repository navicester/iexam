from django import forms
from django.utils.html import escape, escapejs

from .helpers_linkform import LinkFormAdminForm

class WordExpForm(LinkFormAdminForm):
    class Meta:
        verbose_name = 'Word Exp'
        class_name = "WordExp"
        
    id = forms.CharField(max_length=11, label = "id", widget = forms.TextInput(attrs={'readonly':'readonly','disable':True, 'hidden':True})) 
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
