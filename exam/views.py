from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
from .models import ExamLibItem, ExamItem, Paper, ExamResult
from .forms import PaperForm, ExamItemForm, TestItemForm, ExamLibItemForm, ExamLibItemFormSet, ExamItemFormSet, TestItemFormSet
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import Http404
from django import forms
from django.core.urlresolvers import reverse

# Create your views here.

#Examhome -> ExamItem (model)
class ExamItemDetail(DetailView):
	model = ExamItem
	template_name = 'exam/examresultitem_detail.html'

class ExamItemList(ListView):
	queryset = ExamItem.objects.all()
	model = ExamItem
	template_name = 'exam/examresultitem_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ExamItemList, self).get_context_data(*args, **kwargs)
		context["formset"] = ExamItemFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		ExamResult_pk = self.kwargs.get("pk")
		if ExamResult_pk:
			exam_result = get_object_or_404(ExamResult, pk=ExamResult_pk)
			queryset = ExamItem.objects.filter(exam_result=exam_result)
		return queryset


	def post(self, request, *args, **kwargs):
		formset = ExamItemFormSet(request.POST, request.FILES)
		bValid = True
		if formset.is_valid():
			instances = formset.save(commit=False)

			for form in formset:
				if form.is_valid:
					instance = form.save(commit=False)
					if form.cleaned_data['score_result'] == None:
						bValid = False
					else:
						form.save()	
				else:
					bValid = False				
		else:
			bValid = False

		if bValid == True:
			return redirect("examhome")
		else:
			template = 'exam/examresultitem_list.html'
			context = {
				'formset' : formset,
			}
			return render(request, template, context)
			# return redirect("examhome")


# Paper -> Examlib
class PaperList(ListView):
	queryset = Paper.objects.all()
	model = Paper

	def get_context_data(self, *args, **kwargs):
		context = super(PaperList, self).get_context_data(*args, **kwargs)
		# context["formset"] = TestItemFormSet(queryset=self.get_queryset())
		return context
		
class ExamLibItemList(ListView):
	queryset = ExamLibItem.objects.all()
	model = ExamLibItem

	def get_context_data(self, *args, **kwargs):
		context = super(ExamLibItemList, self).get_context_data(*args, **kwargs)
		queryset = self.get_queryset()
		total_score=0
		for object in queryset:
			total_score += object.score
		context["total_score"] = total_score
		context["formset"] = ExamLibItemFormSet(queryset=self.get_queryset())
		context["queryset"] = self.get_queryset(args, kwargs)
		try:
			Paper_pk = self.kwargs.get("pk")
			if Paper_pk:
				paper = get_object_or_404(Paper, pk=Paper_pk)		
				context['paperForm'] = PaperForm(instance = paper)
		except:
			raise Http404
		return context

	def get_queryset(self, *args, **kwargs):
		Paper_pk = self.kwargs.get("pk")
		if Paper_pk:
			paper = get_object_or_404(Paper, pk=Paper_pk)
			queryset = ExamLibItem.objects.filter(paper=paper)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = ExamLibItemFormSet(request.POST, request.FILES)
		paperForm = PaperForm(request.POST, request.FILES)

		if paperForm.is_valid():
			paper = paperForm.save(commit=False)			
			# paper.save() # it will create a new object, maybe the reason is two Form in this view
			paper.id = self.kwargs.get("pk")
			paper.save()		
			paperForm.save_m2m()
			# GET the option value, it's the model id
			# <option value="1" selected="selected">How to ?  </option>
			# print paperForm['ExamLibItem']['select']['option']
			#print request.POST['ExamLibItem']

		if formset.is_valid():
			instances = formset.save(commit=False)
			for form in formset:
				if form.is_valid():
					new_item = form.save(commit=False)
					if new_item.title != '':	 #prevent empty form						
						Paper_pk = self.kwargs.get("pk")
						paper = get_object_or_404(Paper, pk=Paper_pk)
						new_item.save()
						if form in formset.deleted_forms:
							new_item.paper_set.remove(paper)
						else:
							new_item.paper_set.add(paper)

						# form.save_m2m()
						# https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
				
			messages.success(request, "Exam lib item updated.") 
			return redirect("paper")
		template = 'exam/examlibitem_list.html'
		context = {
			'formset' : formset,
			'paperForm' : paperForm
		}
		return render(request, template, context)
		#raise Http404


class ExamLibItemDetail(FormMixin, DetailView):
	model = ExamLibItem
	form_class = ExamLibItemForm
	#template_name = "carts/checkout_view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ExamLibItemDetail, self).get_context_data(*args, **kwargs)
		context["form"] = ExamLibItemForm(instance = self.get_object())
		return context

	def get_object(self, *args, **kwargs):
		ExamLibItem_pk = self.kwargs.get("pk")
		if ExamLibItem_pk:
			examlibitem = get_object_or_404(ExamLibItem, pk=ExamLibItem_pk)
		return examlibitem

	def get_success_url(self):
		return reverse("paper")		

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

#default context object

#Testhome -> TestItem (form)
class TestItemList(ListView):
	queryset = ExamLibItem.objects.all()
	model = ExamLibItem
	template_name = 'exam/testitem_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TestItemList, self).get_context_data(*args, **kwargs)
		context["formset"] = TestItemFormSet(queryset=self.get_queryset(),
											initial=[{'ref_answer': '',}])
		paper_pk = self.kwargs.get("pk")
		paper = get_object_or_404(Paper, pk=paper_pk)
		bExist = False
		try:
			ExamResult.objects.get(paper=paper, user=self.request.user)
			bExist = True
		except:
			bExist = False
		context["bExist"] = bExist
		return context

	def get_queryset(self, *args, **kwargs):
		paper_pk = self.kwargs.get("pk")
		if paper_pk:
			paper = get_object_or_404(Paper, pk=paper_pk)
			queryset = ExamLibItem.objects.filter(paper=paper)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = TestItemFormSet(request.POST, request.FILES)

		if formset.is_valid():
			instances = formset.save(commit=False)

			for form in formset:
				instance = form.save(commit=False)

				paper_pk = self.kwargs.get("pk")

				try:
					paper = get_object_or_404(Paper, pk=paper_pk)
					examLibItem = instance #form.instance can be only called by ModelFormset

					try:
						exam_item, created = ExamItem.objects.get_or_create(ExamLibItem=examLibItem, 
							paper=paper, user=self.request.user)
					except:
						exam_item = ExamItem.objects.create(
							examlibitem=examLibItem, 
							paper=paper, 
							user = self.request.user,
							answer = '',
							exam_result = None,
							score_result  = 1)
					exam_item.answer = form.cleaned_data.get("answer")

					try:
						exam_result, created = ExamResult.objects.get_or_create(
							paper=paper, user=self.request.user)
					except:
						exam_result = ExamResult.objects.create(
							paper=paper, 
							user = self.request.user,
							score  = 1)						
					exam_item.exam_result = exam_result
					exam_item.save()
				except:
					raise Http404
		else:
			print formset.errors
		return redirect("paper")

#default context object_list	


def examhome(request):
	exam_results = ExamResult.objects.filter(user=request.user)
	if request.user.is_superuser:
		exam_results = ExamResult.objects.all()

	context = {
		"exam_results": exam_results
	}

	return render(request, "exam/examresultpaper_list.html", context)

def testhome(request): #no Model to track test itself. it dynamically generate other Models
	test_papers = Paper.objects.all()

	context = {
		"test_papers": test_papers
	}

	return render(request, "exam/testpaper_list.html", context)	