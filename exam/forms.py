from django import forms
from django.forms import (ComboField, 
							ModelForm, Textarea, TextInput, RadioSelect, 
							IntegerField, CharField,SelectMultiple)
from django.forms.models import modelformset_factory
from django.forms import BaseFormSet,BaseModelFormSet, formset_factory

from .models import ExamItem, ExamLibItem, Paper
from django.utils.translation import ugettext_lazy as _

class PaperForm(ModelForm):

	class Meta:
		model = Paper 
		fields = [
			'ExamLibItem',
			'total_score'
		]

    # OPTIONS = (
    #         ("AUT", "Austria"),
    #         ("DEU", "Germany"),
    #         ("NLD", "Neitherlands"),
    #         )			
	# ExamLibItem = forms.MultipleChoiceField(
	# 	label="Exam Lib Items", 
	# 	widget=SelectMultiple(attrs={'cols': 10, 'rows': 3}), 
	# 	required=False,
	# 	choices=ExamLibItem.objects.all()[0]) 

# https://my.oschina.net/hevakelcj/blog/383185
# http://stackoverflow.com/questions/15393134/django-how-can-i-create-a-multiple-select-form

class ExamLibItemForm(ModelForm):
	class Meta:
		model = ExamLibItem

		exclude = [
			'timestamp',
		]

        error_messages = {
            'contributor' : {
                'required' : _("Hey yow! this field is required!")
            }
        }

	title = CharField(label="Title", widget=Textarea(attrs={'cols': 10, 'rows': 2}), required=True) 
	ref_answer = CharField(label="Reference Answer", widget=Textarea(attrs={'cols': 10, 'rows': 3}), required=True) 
	a = CharField(label="A", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=False) 
	b = CharField(label="B", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=False) 
	c = CharField(label="C", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=False) 
	d = CharField(label="D", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=False) 				
	source = CharField(label="Source", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=True) 
	contributor = CharField(label="Contributor", widget=Textarea(attrs={'cols': 10, 'rows': 1}), required=True) 
				
class ExamItemForm(ModelForm):

	answer = CharField(label="Your Answer", widget=Textarea(attrs={'cols': 10, 'rows': 5}), required=False) 

	class Meta:
		model = ExamItem

		exclude = [
			'user',
			'paper',
			'exam_result',
			'ExamLibItem'
		]

		# looks below didn't take effect ???????????
        widgets = {
            'answer': forms.TextInput(attrs={'cols': 10, 'rows': 50, 'readonly':'readonly','disable':True}),
        }

	def clean_score_result(self):
		if self.cleaned_data.get("score_result") == None:
			raise forms.ValidationError("Score Result can't be empty.")


class TestItemForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(TestItemForm, self).__init__(*args, **kwargs)

	class Meta:
		model = ExamLibItem

		fields = [
			# 'ref_answer'
		]

class ExamLibItemModelFormSet(BaseModelFormSet):
	def is_valid(self):
		return super(ExamLibItemModelFormSet, self).is_valid()

class TestModelFormSet(BaseModelFormSet):
	def is_valid(self):
		return super(TestModelFormSet, self).is_valid()

	def add_fields(self, form, index):
	    super(TestModelFormSet, self).add_fields(form, index)
	    form.fields["answer"] = forms.CharField(
	    		label="Your Answer", 
	    		widget = forms.Textarea(attrs={'cols': 10, 'rows': 5,}) , 
	    		required=False)

TestItemFormSet = modelformset_factory(ExamLibItem, 
											form=TestItemForm, 
											formset=TestModelFormSet, 
											extra=0)   
ExamItemFormSet = modelformset_factory(ExamItem, form=ExamItemForm, extra=0)   
ExamLibItemFormSet = modelformset_factory(ExamLibItem, 
											form=ExamLibItemForm, 
											formset=ExamLibItemModelFormSet, 
											extra=1,
											can_delete=True)   
# https://docs.djangoproject.com/en/1.10/topics/forms/formsets/#can-delete
