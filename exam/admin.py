from django.contrib import admin
from .models import ExamLibItem, Paper, ExamItem, ExamResult

# Register your models here.

class ExamItemInline(admin.TabularInline):
	model = ExamItem
	extra = 0

class ExamLibItemAdmin(admin.ModelAdmin):

	class Meta:
		model = ExamLibItem

class PaperAdmin(admin.ModelAdmin):
	list_display = ('id','name','type','__unicode__')
	filter_horizontal = ['examlibitem']

	class Media:
	    css = {
	        "all": ("admin/extra/css/changelists.css",)
	    }

	class Meta:
		model = Paper

	inlines = [
		ExamItemInline
	]

class ExamItemAdmin(admin.ModelAdmin):

	list_display = ('paper','examlibitem','answer','score_result','user',)
	search_fields = ('examlibitem__title','score_result')
	list_filter = ('user','score_result',)
	ordering = ('user__email','score_result')

	class Meta:
		model = ExamItem

class ExamResultAdmin(admin.ModelAdmin):
	inlines = [
		ExamItemInline
	]
	class Meta:
		model = ExamResult				

admin.site.register(ExamLibItem, ExamLibItemAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(ExamItem, ExamItemAdmin)
admin.site.register(ExamResult, ExamResultAdmin)