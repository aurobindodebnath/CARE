from django.contrib import admin
from .models import ApplicationSecurity, VAPTAssessment, ConfigurationReview, Organization, Department, UserProfile, AppSecComments, VAPTComments, ConfigComments
# Register your models here.

admin.site.register(ApplicationSecurity)
admin.site.register(VAPTAssessment)
admin.site.register(ConfigurationReview)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(AppSecComments)
admin.site.register(VAPTComments)
admin.site.register(ConfigComments)