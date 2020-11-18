from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from activities.models import *

ACCESSIBILITY_CHOICES = (
	(None,'Select application\'s accessibility...'),
	('internal', 'Internal'),
	('external', 'External'),
)
ENVIRONMENT_CHOICES = (
	(None, 'Select testing environment...'),
	('uat', 'UAT'),
	('prod', 'Production'),
)

class RequestApplicationSecurity(forms.Form):
	TESTING_CHOICES = (
		(None, '----------'),
		('blackbox','Black Box'),
		('greybox', 'Grey Box'),
		('whitebox', 'White Box'),
	)
	DEVELOPMENT_CHOICES = (
		(None,'Select development mode...'),
		('inhouse','In-House'),
		('third_party', 'Third Party'),
	)
	CATEGORY_CHOICES = (
		(None, 'Select application type...'),
		('webapp','Web Application'),
		('webservice', 'Web Service'),
		('mobileapp', 'Mobile Application'),
	)
	name = forms.CharField(label='Application Name',  widget=forms.TextInput(attrs={'placeholder':"Enter the name of application..."}))
	category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES, initial=None)
	owner = forms.CharField(label='Application Owner',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter owner name, email and contact no...'}), required=False)
	spoc = forms.CharField(label='Division SPOC',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Division SPOC detail...'}), required=False)
	url = forms.CharField(label='Application URL',  widget=forms.TextInput(attrs={'placeholder':"Enter application's URL..."}))
	role_count = forms.IntegerField(label="No. of roles", help_text="Enter number of roles in application...", initial=0, required=False)
	functionality = forms.CharField( widget=forms.Textarea(attrs={'rows':4, 'placeholder':"Describe application's functionality..."}), required=False)
	testing_type = forms.ChoiceField(label='Testing Type', choices=TESTING_CHOICES, help_text='Select type of testing to be performed...', initial=None)
	accessibility = forms.ChoiceField(label='Application Accessibility', choices=ACCESSIBILITY_CHOICES, initial=None)
	development = forms.ChoiceField(label='Application Development', choices=DEVELOPMENT_CHOICES, initial=None, required=False)
	environment = forms.ChoiceField(label='Application Environment', choices=ENVIRONMENT_CHOICES, initial=None, required=False)
	loc = forms.IntegerField(label="Lines of Code (approx.)", help_text="Enter aprox. lines of code...", initial=0, required=False)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'placeholder':"Add comments..."}), required=False)

	#TODO: Sanatize input

class RequestVaptAssessment(forms.Form):
	
	#task_code = forms.CharField(help_text="Enter unique application code for reference...")
	ip_address = forms.CharField(label='IP Address',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Devices IP address(s) or subnet...'}))
	accessibility = forms.ChoiceField(choices=ACCESSIBILITY_CHOICES, initial=None)
	owner = forms.CharField(label='Asset/Device Owner',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter owner name, email and contact no...'}), required=False)
	spoc = forms.CharField(label='Division SPOC',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Division SPOC details...'}), required=False)
	device_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter device type...'}), required=False)
	environment = forms.ChoiceField(choices=ENVIRONMENT_CHOICES, initial=None, required=False) 
	location = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Enter site location...'}), required=False)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'placeholder':'Add any additional comments...'}), required=False)

	#TODO: Sanatize input

class RequestConfigReview(forms.Form):
#	task = forms.text_field(Task, on_delete=models.CASCADE)
	ip_address = forms.CharField(label='IP Address', widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'IP Address/Hostname...'}))
	owner = forms.CharField(label='Asset/Device Owner', widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'Asset owner\'s name & department...'}), required=False)
	spoc = forms.CharField(label='Division SPOC', widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Division SPOC name, email-id & contact no...'}), required=False)
	device_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Eg Router, Switch, Server, Database...'}), required=False)
	location = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Site location, eg: MKHO, Mumbai...'}), required=False)
	host_count = forms.IntegerField(label='No. of Hosts', initial=0, required=False)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'placeholder':'Add any additional comments...'}), required=False)
	
	#TODO: Sanatize input

class UpdateTask(forms.Form):
	STATUS_CHOICE = (
		('not_assigned', 'Not Assigned'),
		('in_progress', 'In Progress'),
		('completed', 'Completed'),
		('rejected', 'Rejected'),
	)
	USERS_CHOICE = [
		(None, '----------'),
	]
	for up in UserProfile.objects.filter(department__organization__name__exact="KPMG"):
		USERS_CHOICE += [(up.pk, str(up.user.first_name + " " + up.user.last_name + " (" + up.department.organization.name + ")"))]
	assigned_to = forms.ChoiceField(choices=USERS_CHOICE)
	status = forms.ChoiceField(choices=STATUS_CHOICE)

class ActivityUploadForm(forms.ModelForm):
	class Meta:
		model = BulkActivity
		fields = ('category', 'files')
		labels = {
			'category': _('Activity Category'),
			'files': _('Upload')
		}

#class ActivityUploadForm(forms.Form):
#	ACTIVITY_CHOICE = (
#		(None, '-----------------'),
#		('app_sec', 'Penetration Testing'),
#		('vapt', 'Vulnerability Assessment'),
#		('config_review', 'Configuration Audit'),
#	)

#	activity = forms.ChoiceField(label='Activity Type', choices=ACTIVITY_CHOICE)
#	files = forms.FileField(label='Upload')
