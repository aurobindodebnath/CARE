from django.contrib import admin
from .models import * #ApplicationSecurity, VAPTAssessment, ConfigurationReview, Organization, Department, UserProfile, AppSecComments, VAPTComments, ConfigComments

admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Organization)

admin.site.register(Task)
admin.site.register(Comment)

admin.site.register(ApplicationSecurity)
admin.site.register(VAPTAssessment)
admin.site.register(ConfigurationReview)
