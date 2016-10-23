from django import forms
from django.forms import ModelForm, Textarea, TextInput, RadioSelect, IntegerField, CharField
from django.forms.models import modelformset_factory
from django.forms import BaseFormSet,BaseModelFormSet, formset_factory

from .models import ExamItem, ExamLibItem

# https://docs.djangoproject.com/en/1.10/topics/forms/formsets/
# https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/#model-formsets

class ExamItemForm(ModelForm):
	class Meta:
		model = ExamItem

		exclude = [
			"answer",
			'exam_result',
		]
        widgets = {
            # '__title__': Textarea(attrs={'cols': 80, 'rows': 20}),
            'answer': TextInput(attrs={'readonly':'readonly','disable':True}),
        }		

	# def clean_full_name(self):
	# 	full_name = self.cleaned_data.get('full_name')
	# 	#write validation code.
	# 	return full_name

# class ExamLibItemNonModelForm(forms.Form):
# 	pass

class ExamLibItemForm(ModelForm):

	# title = ModelMultipleChoiceField(
	 #  	queryset=Item.objects.all(), 
	 #  	required=True, 
	 #  	widget=SelectMultiple(attrs={"style":"width:500px",}), 
	 #  	help_text="Coloque o Tipo de Medida - Requerido")

	# title   = IntegerField(
	# 		label="title", 
	# 		required=True, 
	# 		help_text="Coloque a Quantidade - Requerido")
	# a   = IntegerField(
	# 		label="a", 
	# 		required=True, 
	# 		help_text="Coloque a Quantidade - Requerido")      
	# b   = IntegerField(
	# 		label="b", 
	# 		required=True, 
	# 		help_text="Coloque a Quantidade - Requerido")
	# c   = IntegerField(
	# 		label="c", 
	# 		required=True, 
	# 		help_text="Coloque a Quantidade - Requerido")
	# d   = IntegerField(
	# 		label="d", 
	# 		required=True, 
	# 		help_text="Coloque a Quantidade - Requerido")

	# ref_answer   = Textarea(required=False)  
	ref_answer   = CharField(label="Your Answer", widget=Textarea(attrs={'cols': 10, 'rows': 5}), required=False)    		      		      		      
	# b   = ModelMultipleChoiceField(
	# 		queryset=Produto.objects.all(), 
	# 		widget=SelectMultiple(attrs={"style":"width:500px",}), 
	# 		required=True, 
	# 		help_text="Escolha o Produto - Requerido")

	def __init__(self, *args, **kwargs):
		super(ExamLibItemForm, self).__init__(*args, **kwargs)
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
		super(ExamLibItemForm, self)._clean_fields()
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

	# def is_valid(self):
	# 	return True

	class Meta:
		model = ExamLibItem

		fields = [
			# 'title',
			# 'a',
			# 'b',
			# 'c',
			# 'd',
			'ref_answer'
		]

        # widgets = {
        #     'title': Textarea(attrs={'cols': 80, 'rows': 20}),
        #     'a': RadioSelect,
        #     'ref_answer': forms.TextInput(attrs={'readonly':'readonly','disable':True}),
        # }				
    #


class ExamModelFormSet(BaseModelFormSet):
	def is_valid(self):
		return super(ExamModelFormSet, self).is_valid()

	def add_fields(self, form, index):
	    super(ExamModelFormSet, self).add_fields(form, index)
	    form.fields["add_field"] = forms.CharField(
	    		label="Comments", 
	    		widget = forms.TextInput(attrs={'readonly':'readonly','disable':True}) , 
	    		required=False)

ExamLibItemFormSet = modelformset_factory(ExamLibItem, form=ExamLibItemForm, formset=ExamModelFormSet, extra=0)   
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

# ExamLibItemFormSet = formset_factory(ExamLibItemForm, formset=BaseFormSet)

