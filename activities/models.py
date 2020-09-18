from django.db import models
from django.contrib.auth.models import User

### AUTH

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

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user= models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='user_organization', blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, related_name='user_designation', blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.user.username + self.user.email


### CATEGORIES

class ApplicationSecurity(models.Model):
    name = models.CharField(max_length=300)
    url = models.URLField(max_length=300)
    functionality = models.TextField()
    business_purpose = models.TextField()
    no_of_roles = models.CharField(max_length=200)
    number_of_lines_of_code = models.CharField(max_length=200)
    host_server = models.CharField(max_length=200)
    technologies = models.CharField(max_length=300)
    application_db_details = models.CharField(max_length=200)
    
    credentials = models.TextField()
    other_details = models.TextField()

    STATUS_CHOICES = (
        ('Not Assigned','Not Assigned'),
        ('Rejected','Rejected'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    )

    assigned_by = models.ForeignKey(User, related_name='application_assigned_by', blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, related_name='application_assigned_to',blank=True, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class VAPTAssessment(models.Model):
    name = models.TextField()
    ip_addresses = models.TextField()
    device_type = models.TextField()
    other_details = models.TextField()

    STATUS_CHOICES = (
        ('Not Assigned','Not Assigned'),
        ('Rejected','Rejected'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    )

    assigned_by = models.ForeignKey(User,  related_name='vapt_assigned_by', blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, related_name='vapt_assigned_to', blank=True, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class ConfigurationReview(models.Model):
    name = models.CharField(max_length=300)
    DEVICE_CHOICES = (
        ('Router','Router'),
        ('Switches','Switches'),
        ('Firewall','Firewall'),
        ('Server-Windows','Server-Windows'),
        ('Server-Linux','Server-Linux'),
        ('Database','Database'),
    )
    device_type = models.CharField(max_length=100,choices=DEVICE_CHOICES)
    host_count = models.IntegerField()
    other_details = models.TextField()

    STATUS_CHOICES = (
        ('Not Assigned','Not Assigned'),
        ('Rejected','Rejected'),
        ('In Progress','In Progress'),
        ('Completed','Completed'),
    )

    assigned_by = models.ForeignKey(User, related_name='config_assigned_by', blank=True, null=True, on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(User, related_name='config_assigned_to', blank=True, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

### COMMENTS

class AppSecComments(models.Model):
    user = models.ForeignKey(User, related_name='appsec_comment_user', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ApplicationSecurity, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)

class VAPTComments(models.Model):
    user = models.ForeignKey(User, related_name='vapt_comment_user', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(VAPTAssessment, related_name='vapt_comment_category', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)

class ConfigComments(models.Model):
    user = models.ForeignKey(User, related_name='config_comment_user', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ConfigurationReview, related_name='config_comment_category', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
