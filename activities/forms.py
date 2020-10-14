from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from activities.models import *

ACCESSIBILITY_CHOICES = (
	('internal', 'Internal'),
	('external', 'External'),
)
ENVIRONMENT_CHOICES = (
	('uat', 'UAT'),
	('prod', 'Production'),
)

class RequestApplicationSecurity(forms.Form):
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
		('webappext','Web Application External'),
		('webappint', 'Web Application Internal'),
		('webserint', 'Web Service External'),
		('webserint', 'Web Service Internal'),
		('mobapp', 'Mobile Application'),
	)
	name = forms.CharField(label='Application Name', help_text="Enter the name of application...")
	category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES)
	owner = forms.CharField(label='Application Owner', help_text='Enter owner name, email and contact no...')
	spoc = forms.CharField(label='Division SPOC', help_text='Enter Division SPOC detail...')
	url = forms.CharField(label='Application URL', help_text="Enter application's URL...")
	role_count = forms.CharField(label="No. of roles", help_text="Enter number of roles in application...")
	functionality = forms.CharField(help_text="Describe application's functionality...")
	testing_type = forms.ChoiceField(label='Testing Type', choices=TESTING_CHOICES, help_text='Select type of testing to be performed...')
	accessibility = forms.ChoiceField(label='Application Accessibility', choices=ACCESSIBILITY_CHOICES, help_text='Select application accessibility...')
	development = forms.ChoiceField(label='Application Development', choices=DEVELOPMENT_CHOICES, help_text='Select development...')
	environment = forms.ChoiceField(label='Application Environment', choices=ENVIRONMENT_CHOICES, help_text='Select testing environment...')
	page_count = forms.IntegerField(label='No. of Static Page', help_text='Enter the no. of static pages...')
	loc = forms.IntegerField(label="Lines of Code", help_text="Enter aprox. lines of code...")
	files = forms.FileField(required=False, label='Upload')
	comments = forms.CharField(required=False, widget=forms.Textarea, help_text="Add comments...")

	#TODO: Sanatize input

class RequestVaptAssessment(forms.Form):
	
	#task_code = forms.CharField(help_text="Enter unique application code for reference...")
	ip_address = forms.CharField(label='IP Address', help_text='Enter Devices IP address(s) or subnet...')
	accessibility = forms.ChoiceField(choices=ACCESSIBILITY_CHOICES, help_text='Select application accessibility...')
	owner = forms.CharField(label='Asset/Device Owner', help_text='Enter owner name, email and contact no...')
	spoc = forms.CharField(label='Division SPOC', help_text='Enter Division SPOC details...')
	device_type = forms.CharField(help_text='Enter device type...')
	environment = forms.ChoiceField(choices=ENVIRONMENT_CHOICES, help_text='Select testing environment...')
	location = forms.CharField(help_text='Enter site location...')
	files = forms.FileField(required=False, label='Upload')
	comments = forms.CharField(required=False, widget=forms.Textarea, help_text="Add comments...")

	#TODO: Sanatize input

class RequestConfigReview(forms.Form):
#	task = forms.text_field(Task, on_delete=models.CASCADE)
	ip_address = forms.CharField(label='IP Address', widget=forms.TextInput(attrs={'placeholder': 'IP Address/Hostname'}))
	owner = forms.CharField(label='Asset/Device Owner', widget=forms.TextInput(attrs={'placeholder': 'Asset owner\'s name & department'}))
	spoc = forms.CharField(label='Division SPOC', widget=forms.TextInput(attrs={'placeholder':'Division SPOC name, email-id & contact no'}))
	device_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Eg Router, Switch, Server, Database'}))
	location = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Site location, eg: MKHO, Mumbai'}))
	host_count = forms.IntegerField(label='No. of Hosts')
	files = forms.FileField(required=False, label='Upload')
	comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Add any additional comments'}))
	
	#TODO: Sanatize input

class UpdateTask(forms.Form):
	STATUS_CHOICE = (
		('not_assigned', 'Not Assigned'),
		('in_progress', 'In Progress'),
		('completed', 'Completed'),
		('rejected', 'Rejected'),
	)
	assigned_to = forms.ChoiceField(choices=[(up.id, str(up.user.first_name + " " + up.user.last_name)) for up in UserProfile.objects.filter(department__organization__name__exact="KPMG")])
	status = forms.ChoiceField(choices=STATUS_CHOICE)
