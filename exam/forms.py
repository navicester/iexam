from django import forms
from django.forms import ModelForm, Textarea, TextInput, RadioSelect, IntegerField, CharField
from django.forms.models import modelformset_factory
from django.forms import BaseFormSet,BaseModelFormSet, formset_factory

from .models import ExamItem, ExamLibItem

# https://docs.djangoproject.com/en/1.10/topics/forms/formsets/
# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/#model-formsets

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
            # 'ExamLibItem' : forms.CharField(max_length=11, label = "ExamLibItem", required=False, 
            # 	widget = forms.SelectMultiple(attrs={'readonly':'readonly','disable':True}))
        }		


# class ExamLibItemNonModelForm(forms.Form):
# 	pass

class TestItemForm(ModelForm):

	# title = ModelMultipleChoiceField(
	 #  	queryset=Item.objects.all(), 
	 #  	required=True, 
	 #  	widget=SelectMultiple(attrs={"style":"width:500px",}), 
	 #  	help_text="Coloque o Tipo de Medida - Requerido")

	# ref_answer   = Textarea(required=False)  
	ref_answer   = CharField(label="Your Answer", widget=Textarea(attrs={'cols': 10, 'rows': 5}), required=False)    		      		      		      

	def __init__(self, *args, **kwargs):
		super(TestItemForm, self).__init__(*args, **kwargs)
		# # without the next line label_from_instance does NOT work 
		# self.fields['title'].queryset = Produto.objects.all()
		# self.fields['title'].label_from_instance = lambda Produto: "%s" % (Produto.produto)

		# self.fields['tipo_id'].queryset = Item.objects.all()
		# self.fields['tipo_id'].label_from_instance = lambda Item: "%s" % (Item.tipo)

	# def clean_ref_answer(self):
	# 	self.cleaned_data['ref_answer'] = "default answer"
	# 	ref_answer_value = self.cleaned_data.get('ref_answer')
	# 	if ref_answer_value != "":
	# 		self.cleaned_data['ref_answer'] = ref_answer_value

	def clean(self):
		if self.cleaned_data.get("ref_answer") is None:
			self.cleaned_data['ref_answer'] = "ref_answer_value"

	def _clean_fields(self):
		super(TestItemForm, self)._clean_fields()
	    # for name, field in self.fields.items():
	    #     # value_from_datadict() gets the data from the data dictionaries.
	    #     # Each widget type knows how to retrieve its own data, because some
	    #     # widgets split data over several HTML fields.
	    #     if field.disabled:
	    #         value = self.initial.get(name, field.initial)
	    #     else:
	    #         value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
	    #     try:
	    #         if isinstance(field, FileField):
	    #             initial = self.initial.get(name, field.initial)
	    #             value = field.clean(value, initial)
	    #         else:
	    #             value = field.clean(value)
	    #         self.cleaned_data[name] = value
	    #         if hasattr(self, 'clean_%s' % name):
	    #             value = getattr(self, 'clean_%s' % name)()
	    #             self.cleaned_data[name] = value
	    #     except ValidationError as e:
	    #         self.add_error(name, e)

	def is_valid(self):
		super(TestItemForm, self).is_valid()

	class Meta:
		model = ExamLibItem

		fields = [
			'ref_answer'
		]

class TestItemFormSet(BaseModelFormSet):
	def is_valid(self):
		return super(TestItemFormSet, self).is_valid()

	def add_fields(self, form, index):
	    super(TestItemFormSet, self).add_fields(form, index)
	    form.fields["add_field"] = forms.CharField(
	    		label="Comments", 
	    		widget = forms.TextInput(attrs={'readonly':'readonly','disable':True}) , 
	    		required=False)

class ExamModelFormSet(BaseModelFormSet):
	def is_valid(self):
		return super(ExamModelFormSet, self).is_valid()

	def add_fields(self, form, index):
	    super(ExamModelFormSet, self).add_fields(form, index)
	    form.fields["ref_answer"] = forms.CharField(
	    		label="ref_answer", 
	    		widget = forms.TextInput(attrs={'readonly':'readonly','disable':True}) , 
	    		required=False)

TestItemFormSet = modelformset_factory(ExamLibItem, form=TestItemForm, formset=ExamModelFormSet, extra=0)   
ExamItemFormSet = modelformset_factory(ExamItem, form=ExamItemForm, extra=0)   


# class BaseFormSet(BaseFormSet):
#     def clean(self):
#         """Checks that no two articles have the same title."""
#         if any(self.errors):
#             # Don't bother validating the formset unless each form is valid on its own
#             return

#         for form in self.forms:
#             answer = form.cleaned_data['answer']            
#             if answer == '':
#                 raise forms.ValidationError("answer can't be empty.")

# TestItemFormSet = formset_factory(TestItemForm, formset=BaseFormSet)

