from django.db import models
from django.contrib.auth.models import User

# Authentication & User model

#TODO: create proper __str__ functions

class Organization(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
	contact = models.CharField(max_length=16)
	department = models.ForeignKey(Department, related_name='user_designation', blank=True, null=True, on_delete=models.SET_NULL)
	organization = models.ForeignKey(Organization, related_name='user_organization', blank=True, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.user.username + self.user.email


# Task Model

class Task(models.Model):
	STATUS_CHOICES = (
		('Not Assigned','Not Assigned'),
		('Rejected','Rejected'),
		('In Progress','In Progress'),
		('Completed','Completed'),
	)

	task_code = models.CharField(max_length=100) #or name
	assigned_by = models.ForeignKey(UserProfile, related_name='application_assigned_by', on_delete=models.PROTECT)
	date_posted = models.DateTimeField(auto_now_add=True)
	assigned_to = models.ForeignKey(UserProfile, related_name='application_assigned_to', blank=True, on_delete=models.PROTECT)
	#why as foreign key? 
	#Is the tester supposed to have access to portal?
	# if so, then account has to be created for each any every tester to whom the job is assigned
	status = models.CharField(max_length=100, choices=STATUS_CHOICES)

	def __str__(self):
		return self.name

class Comment(models.Model):
	task_name = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(UserProfile, related_name='comment_user', null=True, blank=False, on_delete=models.SET_NULL)
	date = models.DateTimeField(auto_now=True)
	comment = models.TextField(max_length=500)

	def __str__(self):
		return self.name

class ApplicationSecurity(models.Model):
	task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)							#can be removed
	url = models.URLField(max_length=300)
	functionality = models.TextField(max_length=500)
	business_purpose = models.TextField(max_length=500)
	role_count = models.CharField(max_length=200) 					#no. of roles
	loc = models.CharField(max_length=200) 							#lines of code
	host_server = models.CharField(max_length=200)
	technologies_frontend = models.CharField(max_length=500) 		#or simple tech
	technolofies_backend = models.CharField(max_length=500)  		#application db details

	credentials = models.TextField()								#TODO: create seperate table for credentials
	comments = models.TextField(max_length=500)

	def __str__(self):
		return self.name
   
class VAPTAssessment(models.Model):
	task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.TextField()										#can be removed
	ip_addresses = models.TextField()								#do seperate record has to be created for each IP or IPs can be assigned in bulk
	device_type = models.TextField()								#should be choice field
	comments = models.TextField()

	def __str__(self):
		return self.name


class ConfigurationReview(models.Model):
	DEVICE_CHOICES = (
		('Router','Router'),
		('Switches','Switches'),
		('Firewall','Firewall'),
		('Server-Windows','Server-Windows'),
		('Server-Linux','Server-Linux'),
		('Database','Database'),
	)
	task_name = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)							#can be removed
	device_type = models.CharField(max_length=100, choices=DEVICE_CHOICES)
	host_count = models.IntegerField()								#????
	comments = models.TextField()

	def __str__(self):
		return self.name
