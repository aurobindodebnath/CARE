from django.contrib import admin
from .models import UserProfile, Organization, Department

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Department)
