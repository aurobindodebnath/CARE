from django.db import models
from django.contrib.auth.models import User

# Authentication & User model

#TODO: create proper __str__ functions
#TODO: check on_delete option
#TODO: add help_text as per requirement

ACCESSIBILITY_CHOICES = (
	('internal', 'Internal'),
	('external', 'External'),
)
ENVIRONMENT_CHOICES = (
	('uat', 'UAT'),
	('prod', 'Production'),
)

class Organization(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=150)
	full_name = models.CharField(max_length=240)
	organization = models.ForeignKey(Organization, related_name='department_organization', on_delete=models.PROTECT)
	location = models.CharField(max_length=120)
	address = models.TextField()

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	#TODO: Assign roles to UserProfile
	user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
	employee_id = models.CharField(max_length=50)
	contact = models.CharField(max_length=16)
	department = models.ForeignKey(Department, related_name='user_designation', on_delete=models.PROTECT)
#	organization = models.ForeignKey(Organization, related_name='user_organization', on_delete=models.PROTECT)

	def __str__(self):
		return self.user.username


# Task Model

class Task(models.Model):
	STATUS_CHOICES = (
		('not_assigned','Not Assigned'),
		('rejected','Rejected'),
		('in_progress','In Progress'),
		('completed','Completed'),
	)

	code = models.CharField(max_length=100)
	assigned_by = models.ForeignKey(UserProfile, related_name='application_assigned_by', on_delete=models.PROTECT)
	date_posted = models.DateTimeField(auto_now_add=True)
	assigned_to = models.ForeignKey(UserProfile, related_name='application_assigned_to',null=True, blank=True, on_delete=models.PROTECT)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True, default='not_assigned')

	def __str__(self):
		return self.code

class Comment(models.Model):
	task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(UserProfile, related_name='comment_user', null=True, blank=False, on_delete=models.SET_NULL)
	date = models.DateTimeField(auto_now=True)
	comment = models.TextField(max_length=500)

	def __str__(self):
		return self.task.code

class ApplicationSecurity(models.Model):
	TESTING_CHOICES = (
		('blackbox','Black Box'),
		('greybox', 'Grey Box'),
		('whitebox', 'White Box'),
	)
	DEVELOPMENT_CHOICES = (
		('inhouse','In-House'),
		('third_party', 'Third Party'),
	)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	owner = models.TextField(null=True)
	spoc = models.TextField(null=True)
	url = models.URLField(max_length=300, null=True)
	role_count = models.CharField(max_length=200, null=True)
	functionality = models.TextField(max_length=500, null=True)
	testing_type = models.TextField(max_length=50, choices=TESTING_CHOICES, null=True)
	accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES, null=True)
	development = models.CharField(max_length=20, choices=DEVELOPMENT_CHOICES, null=True)
	environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES, null=True)
	page_count = models.IntegerField(null=True)
	loc = models.CharField(max_length=200, null=True)
	files = models.FileField(upload_to='uploads/penetration_testing/', null=True, blank=True)
	comments = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.task.code
   
class VaptAssessment(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	ip_address = models.TextField(null=True)
	accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES, null=True)
	owner = models.TextField(null=True)
	spoc = models.TextField(null=True)
	device_type = models.TextField(null=True)
	environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES, null=True)
	location = models.TextField(null=True)
	files = models.FileField(upload_to='uploads/vulnerability_assessment/', null=True, blank=True)
	comments = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.task.code


class ConfigurationReview(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	ip_address = models.TextField(null=True)
	owner = models.TextField(null=True)
	spoc = models.TextField(null=True)
	device_type = models.TextField(null=True)
	location = models.TextField(null=True)
	host_count = models.IntegerField(null=True)
	files = models.FileField(upload_to='uploads/configguration_review/', null=True, blank=True)
	comments = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.task.code
