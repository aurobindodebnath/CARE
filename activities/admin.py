from django.contrib import admin
from .models import ApplicationSecurity, VAPTAssessment, ConfigurationReview
# Register your models here.

admin.site.register(ApplicationSecurity)
admin.site.register(VAPTAssessment)
admin.site.register(ConfigurationReview)