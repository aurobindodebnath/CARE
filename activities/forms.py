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
		(None, 'Select testing type...'),
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
	CRITICAL_CHOICES = (
#		(None, 'Does application store critical data?'),
		('y', 'Yes'),
		('n', 'No'),
	)
	name = forms.CharField(label='*Application Name',  widget=forms.TextInput(attrs={'placeholder':"Enter the name of application..."}))
	url = forms.CharField(label='*Application URL',  widget=forms.Textarea(attrs={'rows':2, 'placeholder':"Enter application's(or APK/IPA) URL..."}))
#	item_count = forms.IntegerField(label='*Item Count', help_text='Enter number of items in activity...', initial=1)
	category = forms.ChoiceField(label='*Application Type', choices=CATEGORY_CHOICES, initial=None)
	accessibility = forms.ChoiceField(label='*Application Accessibility', choices=ACCESSIBILITY_CHOICES, initial=None)
	testing_type = forms.ChoiceField(label='*Testing Type', choices=TESTING_CHOICES, initial=None)
	environment = forms.ChoiceField(label='*Application Environment', choices=ENVIRONMENT_CHOICES, initial=None)
	development = forms.ChoiceField(label='Application Development', choices=DEVELOPMENT_CHOICES, initial=None, required=False)
	critical = forms.ChoiceField(label='*Critical Application', choices=CRITICAL_CHOICES, initial='n')
	functionality = forms.CharField( widget=forms.Textarea(attrs={'rows':4, 'placeholder':"Describe application's functionality..."}), required=False)
	role_count = forms.IntegerField(label="No. of roles", help_text="Enter number of roles in application...", initial=0, required=False)
	loc = forms.IntegerField(label="Lines of Code (approx.)", help_text="Enter aprox. lines of code...", initial=0, required=False)
	owner = forms.CharField(label='Application Owner',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter owner name, email and contact no...'}), required=False)
	spoc = forms.CharField(label='Division SPOC',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Division SPOC detail...'}), required=False)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'placeholder':"Enter additional comments (e.g. type of web service/application)..."}), required=False)

	#TODO: Sanatize input

class RequestVaptAssessment(forms.Form):
	name = forms.CharField(label='*Name', widget=forms.TextInput(attrs={'placeholder':'Enter name or IP Range...'}))
	ip_address = forms.CharField(label='*IP Address',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Devices IP address(s) or subnet...'}))
	item_count = forms.IntegerField(label='*Host Count', help_text='Enter number of items in activity...', initial=1)
	accessibility = forms.ChoiceField(label='*Host Accessibility', choices=ACCESSIBILITY_CHOICES, initial=None)
	environment = forms.ChoiceField(choices=ENVIRONMENT_CHOICES, initial=None, required=False) 
	device_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter device type...'}), required=False)
	owner = forms.CharField(label='Asset/Device Owner',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter owner name, email and contact no...'}), required=False)
	spoc = forms.CharField(label='Division SPOC',  widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter Division SPOC details...'}), required=False)
	location = forms.CharField( widget=forms.TextInput(attrs={'placeholder':'Enter site location...'}), required=False)
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows':8, 'placeholder':'Enter additional comments (e.g. Propsed date and time)...'}), required=False)

	#TODO: Sanatize input

class RequestConfigReview(forms.Form):
	name = forms.CharField(label='*Name', widget=forms.TextInput(attrs={'placeholder':'Enter host name or IP Range...'}))
	host_name = forms.CharField(label='*Host Name', widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'IP Address/Hostname...'}))
	item_count = forms.IntegerField(label='*Host Count', help_text='Enter number of items in activity...', initial=1)
	device_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Eg Router, Switch, Server, Database...'}), required=False)
	owner = forms.CharField(label='Asset/Device Owner', widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'Asset owner\'s name & department...'}), required=False)
	spoc = forms.CharField(label='Division SPOC', widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Division SPOC name, email-id & contact no...'}), required=False)
	location = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Site location, eg: MKHO, Mumbai...'}), required=False)
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
#	for up in UserProfile.objects.filter(department__organization__name__exact="KPMG"):
#		USERS_CHOICE += [(up.pk, str(up.user.first_name + " " + up.user.last_name + " (" + up.department.organization.name + ")"))]
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

class UploadForm(forms.Form):
	excel = forms.FileField(label='*Upload')

#class ActivityUploadForm(forms.Form):
#	ACTIVITY_CHOICE = (
#		(None, '-----------------'),
#		('app_sec', 'Penetration Testing'),
#		('vapt', 'Vulnerability Assessment'),
#		('config_review', 'Configuration Audit'),
#	)

#	activity = forms.ChoiceField(label='Activity Type', choices=ACTIVITY_CHOICE)
#	files = forms.FileField(label='Upload')
