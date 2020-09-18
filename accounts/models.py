from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Organization(models.Model):
    ROLE = (
        ('Vender','Vendor'),
        ('Client','Client'),
        )
    name = models.CharField(max_length=120)
    role = models.CharField(max_length = 100, choices=ROLE)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=120)
    organization = models.ManyToManyField(Organization)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user= models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='user_organization', blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, related_name='user_designation', blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.user.username + self.user.email