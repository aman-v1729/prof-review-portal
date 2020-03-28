from django.contrib import admin
from .models import Department, Prof, Course, Prof_Review, Course_Review, P_Rev_Like, C_Rev_Like, P_Rev_Report, C_Rev_Report
#from users.models import Profile
admin.site.disable_action('delete_selected')

def delete_post(modeladmin, request, queryset):
	for query in queryset:
		p = query.post
		p.delete()
delete_post.short_description = "Delete the selected reported posts"

def delete_all_reportsP(modeladmin, request, queryset):
	for query in queryset:
		p = query.post
		p.reports = 0
		p.save()
		reports = P_Rev_Report.objects.filter(post = p)
		for report in reports:
			report.delete()
delete_all_reportsP.short_description = "Delete all the reports of the selected posts"

def delete_all_reportsC(modeladmin, request, queryset):
	for query in queryset:
		p = query.post
		p.reports = 0
		p.save()
		reports = C_Rev_Report.objects.filter(post = p)
		for report in reports:
			report.delete()
delete_all_reportsC.short_description = "Delete all the reports of the selected posts"


def delete_reportsP(modeladmin, request, queryset):
	for query in queryset:
		query.reports = 0
		query.save()
		reports = P_Rev_Report.objects.filter(post = query)
		for report in reports:
			report.delete()
delete_reportsP.short_description = "Delete all the reports of the selected posts"

def delete_reportsC(modeladmin, request, queryset):
	for query in queryset:
		p = query
		p.reports = 0
		p.save()
		reports = C_Rev_Report.objects.filter(post = p)
		for report in reports:
			report.delete()
delete_reportsC.short_description = "Delete all the reports of the selected posts"

def delete_selected_and_warn(modeladmin,request, queryset):
	for query in queryset:
		p = query.author.profile
		p.warn_offensive = True
		p.save()
		query.delete()

class Prof_ReviewAdmin(admin.ModelAdmin):
	list_display = ['prof', 'author', 'title', 'reports', 'date_posted']
	list_filter = ['date_posted']
	ordering = ['reports', 'date_posted']
	actions = [delete_reportsP, 'delete_selected', delete_selected_and_warn]

class Course_ReviewAdmin(admin.ModelAdmin):
	list_display = ['course', 'author', 'title', 'reports', 'date_posted']
	list_filter = ['date_posted']
	ordering = ['reports', 'date_posted']
	actions = [delete_reportsC, 'delete_selected', delete_selected_and_warn]

class ReportAdminP(admin.ModelAdmin):
	list_display = ['post', 'user']
	actions = [delete_post, delete_all_reportsP]
	ordering = ['post']

class ReportAdminC(admin.ModelAdmin):
	list_display = ['post', 'user']
	actions = [delete_post, delete_all_reportsC]
	ordering = ['post']


#admin.site.register(Department)
admin.site.register(Prof)
admin.site.register(Course)
admin.site.register(Prof_Review, Prof_ReviewAdmin)
admin.site.register(Course_Review, Course_ReviewAdmin)
#admin.site.register(P_Rev_Like)
#admin.site.register(C_Rev_Like)
admin.site.register(P_Rev_Report, ReportAdminP)
admin.site.register(C_Rev_Report, ReportAdminC)