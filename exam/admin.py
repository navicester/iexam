from django.contrib import admin
from .models import ExamLibItem, Paper, ExamItem, ExamResult

# Register your models here.
# class ExamLibItemInline(admin.TabularInline):
# 	model = ExamLibItem

# class ExamLibItemInline(admin.TabularInline):
# 	model = ExamLibItem

class ExamItemInline(admin.TabularInline):
	model = ExamItem
	extra = 0

class ExamLibItemAdmin(admin.ModelAdmin):

	class Meta:
		model = ExamLibItem

class PaperAdmin(admin.ModelAdmin):
	class Meta:
		model = Paper

class ExamItemAdmin(admin.ModelAdmin):

	list_display = ('ExamLibItem','answer','score_result','user',)
	search_fields = ('ExamLibItem__title','score_result')
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