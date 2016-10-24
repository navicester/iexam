from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
from .models import ExamLibItem, ExamItem, Paper, ExamResult
from .forms import ExamItemForm, TestItemForm, ExamItemFormSet, TestItemFormSet
from django.contrib import messages
from django.http import Http404

# Create your views here.
# class TestPaperList(ListView):
# 	queryset = Paper.objects.all()
# 	model = Paper

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(PaperList, self).get_context_data(*args, **kwargs)
# 		# context["formset"] = TestItemFormSet(queryset=self.get_queryset())
# 		return context

class PaperList(ListView):
	queryset = Paper.objects.all()
	model = Paper

	def get_context_data(self, *args, **kwargs):
		context = super(PaperList, self).get_context_data(*args, **kwargs)
		# context["formset"] = TestItemFormSet(queryset=self.get_queryset())
		return context

class ExamItemDetail(DetailView):
	model = ExamItem

class ExamItemList(ListView):
	queryset = ExamItem.objects.all()
	model = ExamItem

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

		if formset.is_valid():
			instances = formset.save(commit=False)

			for form in formset:
				instance = form.save(commit=False)

		return redirect("examhome")
		
class ExamLibItemList(ListView):
	queryset = ExamLibItem.objects.all()
	model = ExamLibItem

	def get_context_data(self, *args, **kwargs):
		context = super(ExamLibItemList, self).get_context_data(*args, **kwargs)
		# context["formset"] = TestItemFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		Paper_pk = self.kwargs.get("pk")
		if Paper_pk:
			paper = get_object_or_404(Paper, pk=Paper_pk)
			queryset = ExamLibItem.objects.filter(paper=paper)
		return queryset


class ExamLibItemDetail(DetailView):
	model = ExamLibItem

#default context object


class TestItemList(ListView):
	queryset = ExamLibItem.objects.all()
	model = ExamLibItem
	template_name = 'exam/testitem_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TestItemList, self).get_context_data(*args, **kwargs)
		context["formset"] = TestItemFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		paper_pk = self.kwargs.get("pk")
		if paper_pk:
			paper = get_object_or_404(Paper, pk=paper_pk)
			queryset = ExamLibItem.objects.filter(paper=paper)
		return queryset

	def post(self, request, *args, **kwargs):
		#if request.method == 'POST':
		formset = TestItemFormSet(request.POST or None, request.FILES)

		print formset.is_valid()

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
						print "get_or_create OK"
					except:
						exam_item = ExamItem.objects.create(
							ExamLibItem=examLibItem, 
							paper=paper, 
							user = self.request.user,
							answer = '',
							exam_result = None,
							score_result  = 1)
						print "get_or_create fail"
					exam_item.answer = form.cleaned_data.get("ref_answer")

					try:
						print paper
						print self.request.user
						print ExamResult.objects.all()
						print ExamItem.objects.all()
						print ExamLibItem.objects.all()
						exam_result, created = ExamResult.objects.get_or_create(
							paper=paper, user=self.request.user)
						print "get_or_create 2 OK"
					except:
						exam_result = ExamResult.objects.create(
							paper=paper, 
							user = self.request.user,
							score  = 1)						
						print "get_or_create 2 fail"
					exam_item.exam_result = exam_result
					print exam_item
					exam_item.save()
					print exam_item
				except:
					raise Http404
		else:
			print formset.errors
		return redirect("paper")

		# if formset.is_valid():
		# 	formset.save(commit=False)
		# 	for form in formset:
		# 		# new_item = form.save(commit=False)

		# 		paper_pk = self.kwargs.get("pk")
		# 		try:
		# 			paper = get_object_or_404(Paper, pk=paper_pk)
		# 			examLibItem = form.instance
		# 			# exam_item = ExamItem.objects.create(ExamLibItem=cart, paper=paper, user = self.request.user)
		# 			exam_item = ExamItem.objects.get_or_create(ExamLibItem=examLibItem, paper=paper, user = self.request.user)[0]
		# 			exam_item.save()

		# 		except:
		# 			raise Http404
				
		# 	messages.success(request, "Your inventory and pricing has been updated.")
		# 	return redirect("paper")
		# raise Http404


#default context object_list	

# class ExamItemCreateView(CreateView):
# 	form_class = UserAddressForm
# 	template_name = "forms.html"
# 	success_url = "/checkout/address/"

# 	def form_valid(self, form, *args, **kwargs):
# 		return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)

def examhome(request):
	exam_results = ExamResult.objects.filter(user=request.user)
	if request.user.is_superuser:
		exam_results = ExamResult.objects.all()

	context = {
		"exam_results": exam_results
	}

	return render(request, "exam.html", context)

def testhome(request): #no Model to track test itself. it dynamically generate other Models
	test_papers = Paper.objects.all()

	context = {
		"test_papers": test_papers
	}

	return render(request, "test.html", context)	