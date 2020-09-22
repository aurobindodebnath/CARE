from django.db import models
from django.contrib.auth.models import User

# Authentication & User model

#TODO: create proper __str__ functions
#TODO: check on_delete option
#TODO: add help_text as per requirement

class Organization(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	#TODO: Assign roles to UserProfile
	user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
	employee_id = models.CharField(max_length=50)
	contact = models.CharField(max_length=16)
	department = models.ForeignKey(Department, related_name='user_designation', on_delete=models.PROTECT)
	organization = models.ForeignKey(Organization, related_name='user_organization', on_delete=models.PROTECT)

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
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	url = models.URLField(max_length=300)
	functionality = models.TextField(max_length=500)
	business_purpose = models.TextField(max_length=500)
	role_count = models.CharField(max_length=200)
	loc = models.CharField(max_length=200)
	host_server = models.CharField(max_length=200)
	frontend_technologies = models.CharField(max_length=500)
	backend_technologies = models.CharField(max_length=500)  		#application db details

	credentials = models.TextField()								#TODO: create seperate table for credentials
	comments = models.TextField(null=True, blank=True, max_length=500)

	def __str__(self):
		return self.task.code
   
class VaptAssessment(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.TextField()
	ip_address = models.TextField()
	device_type = models.TextField()
	comments = models.TextField()

	def __str__(self):
		return self.task.code


class ConfigurationReview(models.Model):
	DEVICE_CHOICES = (
		('router','Router'),
		('switches','Switches'),
		('firewall','Firewall'),
		('window_server','Windows Server'),
		('linux_server','Linux Server'),
		('database','Database'),
		('other', 'Other'),
	)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	device_type = models.CharField(max_length=16, choices=DEVICE_CHOICES)
	host_count = models.IntegerField()
	comments = models.TextField()

	def __str__(self):
		return self.task.code
