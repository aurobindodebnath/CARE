from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from activities.models import *

class RequestApplicationSecurity(forms.Form):
	task_code = forms.CharField(help_text="Enter unique application code for reference...")
	name = forms.CharField(help_text="Enter the name of application...")
	url = forms.CharField(help_text="Enter application's URL...")
	functionality = forms.CharField(help_text="Describe application's functionality...")
	business_purpose = forms.CharField(help_text="Describe application's business purpose...")
	role_count = forms.CharField(label="No. of roles", help_text="Enter number of roles in application...")
	loc = forms.CharField(label="Lines of Code", help_text="Enter aprox. lines of code...")
	host_server = forms.CharField(help_text="Enter host server IP...")
	frontend_technologies = forms.CharField(help_text="Enter details of technologies used by application...")
	backend_technologies = forms.CharField(help_text="Enter details of database used by application...")
	credentials = forms.CharField(help_text="Provide credentials of different roles...")
	comments = forms.CharField(required=False, widget=forms.Textarea, help_text="Add comments...")

	#TODO: Sanatize input

class RequestVaptAssessment(forms.Form):
	task_code = forms.CharField(help_text="Enter unique application code for reference...")
	name = forms.CharField(help_text="Enter the name of application...")
	ip = forms.CharField(help_text="Enter application's IP...")
	device_type = forms.CharField(help_text="Enter device type...")
	comments = forms.CharField(required=False, widget=forms.Textarea, help_text="Add comments...")

	#TODO: Sanatize input

class RequestConfigReview(forms.Form):
	DEVICE_TYPE = (
		('router', 'Router'),
		('switch', 'Switch'),
		('firewall', 'Firewall'),
		('windows_server', 'Windows Server'),
		('linux_server', 'Linux Server'),
		('database', 'Database'),
		('other', 'Other'),
	)

	task_code = forms.CharField(help_text="Enter unique application code for reference...")
	name = forms.CharField(help_text="Enter the name of application...")
	device_type = forms.ChoiceField(choices=DEVICE_TYPE, help_text="Select device type...")
	host_count = forms.IntegerField(initial='1', help_text="Enter no. of host...")
	comments = forms.CharField(required=False, widget=forms.Textarea, help_text="Add comments...")

	#TODO: Sanatize input

class UpdateTask(forms.Form):
	STATUS_CHOICE = (
		('not_assigned', 'Not Assigned'),
		('in_progress', 'In Progress'),
		('completed', 'Completed'),
		('rejected', 'Rejected'),
	)
	assigned_to = forms.ChoiceField(choices=[(up.id, str(up.user.first_name + " " + up.user.last_name)) for up in UserProfile.objects.filter(organization__name__exact="KPMG")])
	status = forms.ChoiceField(choices=STATUS_CHOICE, help_text="Update the stauts of activity....")
