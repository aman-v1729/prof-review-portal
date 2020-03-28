from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Ban
from datetime import datetime, timedelta
# Register your models here.
admin.site.site_header = 'Review Portal'
admin.site.unregister(Group)
admin.site.unregister(User)


def ban_selected_for_span(modeladmin, request, queryset):
	for query in queryset:
		b = Ban()
		b.email = query.email
		b.end = datetime.now() + timedelta(days = 15)
		b.permanent = False
		b.save()
		query.delete()
ban_selected_for_span.short_description = "Ban for 15 days"

def ban_selected_permanent(modeladmin, request, queryset):
	for query in queryset:
		b = Ban()
		b.email = query.email
		b.end = datetime.now() + timedelta(days = 15)
		b.permanent = True
		b.save()
		query.delete()
ban_selected_permanent.short_description = "Ban Permanently"

class UserAdmin(admin.ModelAdmin):
	list_display = ['username', 'email', 'password']
	actions = [ban_selected_for_span, ban_selected_permanent, 'delete_selected']

admin.site.register(User, UserAdmin)


admin.site.register(Profile)
'''
class UserAdmin(admin.ModelAdmin):
	list_display = ['email', 'duration', 'end']
#	actions = [delete_reportsP, 'delete_s


def delete_reportsC(modeladmin, request, queryset):
	for query in queryset:
		p = query
		p.reports = 0
		p.save()
		reports = C_Rev_Report.objects.filter(post = p)
		for report in reports:
			report.delete()
delete_reportsC.short_description = "Delete all the reports of the selected posts"
'''
class BanAdmin(admin.ModelAdmin):
	list_display = ['email', 'end']
#	actions = [delete_reportsP, 'delete_selected']

admin.site.register(Ban, BanAdmin)
