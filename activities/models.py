import os
from datetime import datetime
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
	
	def object2array(self):
		arr = [self.name,]
		return arr

class Department(models.Model):
	name = models.CharField(max_length=150)
	full_name = models.CharField(max_length=240)
	organization = models.ForeignKey(Organization, related_name='department_organization', on_delete=models.PROTECT)
	location = models.CharField(max_length=120)
	address = models.TextField()

	def __str__(self):
		return self.name
	
	def object2array(self):
		arr = [self.name, self.full_name, self.organization.pk, self.location, self.address] 
		return arr

class UserProfile(models.Model):
	#TODO: Assign roles to UserProfile
	user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
	employee_id = models.CharField(max_length=50, null=True, blank=True)
	contact = models.CharField(max_length=16)
	department = models.ForeignKey(Department, related_name='user_designation', on_delete=models.PROTECT)

	def __str__(self):
		return self.user.username
	
	def object2array(self):
		arr = [self.user.pk, self.employee_id, self.contact, self.department.pk]
		return arr


# Task Model

class Task(models.Model):
	STATUS_CHOICES = (
		('not_assigned','Not Assigned'),
		('rejected','Rejected'),
		('in_progress','In Progress'),
		('completed','Completed'),
	)

	code = models.AutoField(primary_key=True)
	assigned_by = models.ForeignKey(UserProfile, related_name='application_assigned_by', on_delete=models.PROTECT)
	date_posted = models.DateTimeField(default=datetime.now())
	assigned_to = models.ForeignKey(UserProfile, related_name='application_assigned_to',null=True, blank=True, on_delete=models.PROTECT)
	status = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True, default='not_assigned')

	def __str__(self):
		return str(self.code)

	def object2array(self):
		arr = [
			self.code,
			self.assigned_by.pk,
			self.date_posted,
			self.assigned_to.pk if self.assigned_to else None,
			self.status]
		return arr

class Comment(models.Model):
	task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='comment_user', null=True, blank=False, on_delete=models.SET_NULL)
	date = models.DateTimeField(auto_now=True)
	comment = models.TextField(max_length=500)

	def __str__(self):
		return str(self.task.code)

	def object2array(self):
		arr = [
			self.task.pk if self.task else None,
			self.user.pk if self.user else None,
			self.date,
			self.comment]
		return arr

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
	CATEGORY_CHOICES = (
		('webapp','Web Application'),
		('webservice', 'Web Service'),
		('mobileapp', 'Mobile Application'),
	)
	CRITICAL_CHOICES = (
		('n', 'No'),
		('y', 'Yes'),
	)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=300)
	url = models.URLField(max_length=300)
	item_count = models.IntegerField(default=1) #for backend only
	category = models.TextField(max_length=50, choices=CATEGORY_CHOICES)
	accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES)
	testing_type = models.TextField(max_length=50, choices=TESTING_CHOICES)
	environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES, null=True, blank=True)
	development = models.CharField(max_length=20, choices=DEVELOPMENT_CHOICES, null=True, blank=True)
	functionality = models.TextField(max_length=500, null=True, blank=True)
	role_count = models.CharField(max_length=200, null=True, blank=True)
	loc = models.CharField(max_length=200, null=True, blank=True) #for Whitebox
	owner = models.TextField(null=True, blank=True)
	spoc = models.TextField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)
	critical = models.CharField(max_length=10, choices=CRITICAL_CHOICES, default='n')

	def __str__(self):
		return str(self.task.code) + ' - ' + self.name

	def object2array(self):
		arr = [
			self.task.pk,
			self.name,
			self.url,
			self.item_count,
			self.category,
			self.accessibility,
			self.testing_type,
			self.environment,
			self.development,
			self.functionality,
			self.role_count,
			self.loc,
			self.owner,
			self.spoc,
			self.comments,
			self.critical,
		]
		return arr
   
class VaptAssessment(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	ip_address = models.TextField()
	item_count = models.IntegerField(default=1)
	accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES)
	environment = models.CharField(max_length=20, choices=ENVIRONMENT_CHOICES, null=True, blank=True)
	device_type = models.TextField(null=True, blank=True)
	owner = models.TextField(null=True, blank=True)
	spoc = models.TextField(null=True, blank=True)
	location = models.TextField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)

	#Proposed Audit date
	#Proposed Audit Time

	def __str__(self):
		return str(self.task.code) + ' - ' + self.ip_address

	def object2array(self):
		arr = [
			self.task.pk,
			self.name,
			self.ip_address,
			self.item_count,
			self.accessibility,
			self.environment,
			self.device_type,
			self.owner,
			self.spoc,
			self.location,
			self.comments,
		]
		return arr

class ConfigurationReview(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	host_name = models.TextField()
	item_count = models.IntegerField(default=1)
	device_type = models.TextField(null=True, blank=True)
	owner = models.TextField(null=True, blank=True)
	spoc = models.TextField(null=True, blank=True)
	location = models.TextField(null=True, blank=True)
	comments = models.TextField(null=True, blank=True)

	def __str__(self):
		return str(self.task.code) + ' - ' + self.device_type
	
	def object2array(self):
		arr = [
			self.task.pk,
			self.name,
			self.host_name,
			self.item_count,
			self.device_type,
			self.owner,
			self.spoc,
			self.location,
			self.comments,
		]
		return arr

class Criticality(models.Model):
	name = models.CharField(max_length=20)

	def object2array(self):
		arr = [self.name,]
		return arr

class Vulnerability(models.Model):
	observation = models.CharField(max_length=100)
	detail = models.TextField()
	affected_module = models.CharField(max_length=200)
	crticality = models.ForeignKey(Criticality, on_delete=models.PROTECT)
	risk = models.TextField()
	recommendation = models.TextField()
	year = models.CharField(max_length=6)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)

	def object2array(self):
		arr = [
			self.observation,
			self.detail,
			self.affected_module,
			self.criticality.pk,
			self.risk,
			self.recommendation,
			self.year,
			self.department.pk,
		]
		return arr

class BulkActivity(models.Model):
	CATEGORY_CHOICE = (
		(None, '----------------'),
		('app_sec', 'Penetration Testing'),
		('vapt', 'Vulnerability Assessment'),
		('config_review','Configuration Audit'),
		('multiple','Multiple Activities'),
	)

	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	category = models.CharField(max_length=50, choices=CATEGORY_CHOICE, default=None)
	files = models.FileField(upload_to='uploads/bulk_upload/')
	
	def filename(self):
		return os.path.basename(self.files.name)

	def object2array(self):
		arr = [
			self.task.pk,
			self.category,
			self.files.url, #files.path
		]
		return arr

class SanitizedUpload(models.Model):
	uploaded_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	date_uploaded = models.DateTimeField(default=datetime.now())
	files = models.FileField(upload_to='uploads/sanitized_upload/')

	def object2array(self):
		arr = [
			self.uploaded_by.pk,
			self.date_uploaded,
			self.files.url, #files.path
		]
		return arr

class BackupTracker(models.Model):
	backedup_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
	date_backedup = models.DateTimeField(default=datetime.now())
	path = models.CharField(max_length=200)

	def object2array(self):
		arr = [
			self.backedup_by.pk,
			self.date_backedup,
			self.path,
		]
		return arr

class RestoreTracker(models.Model):
	restored_by = models.ForeignKey(User, on_delete=models.PROTECT)
	date_restored = models.DateTimeField(default=datetime.now())
	files = models.FileField(upload_to='uploads/restore_upload/')

	def object2array(self):
		arr = [
			self.restored_by.pk,
			self.date_restored,
			self.files.url, #files.path
		]
		return arr
