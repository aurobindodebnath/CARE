from django.contrib import admin
from activities.models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	pass
	#fields
	#list_display = ('User__first_name',)
	#fieldsets

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	pass

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_filter = ('status', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	pass


@admin.register(ApplicationSecurity)
class ApplicationSecurityAdmin(admin.ModelAdmin):
	pass

@admin.register(VaptAssessment)
class VaptAssessmentAdmin(admin.ModelAdmin):
	pass

@admin.register(ConfigurationReview)
class ConfigurationReviewAdmin(admin.ModelAdmin):
	pass
