import magic
from openpyxl import load_workbook
from django.shortcuts import render, get_object_or_404
from activities.models import * 
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from activities.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from .custom import *

def sum(result):
	total = result.aggregate(Sum('item_count'))['item_count__sum']
	if not total:
		return 0
	return total

def custom_login(request):
	if request.method == 'GET':
		logout(request)
		return render(request, 'login.html')
	elif request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			context = {
				'login_message': 'Incorrect username or password.',
			}
			return render(request, 'login.html', context=context)
	return render(request, 'login.html')

def lockout(request):
	context = {
		'login_message': 'Your account has been lockedout after multiple attempts. Please try again after 1 hour.',
		'disable_status': 'disabled',
	}
	return render(request, 'login.html', context=context)

@login_required
def home(request):

	if request.user.groups.filter(name="Vendor").exists():
#		total_object = Task.objects.all()
		app = ApplicationSecurity.objects.all()
		vapt = VaptAssessment.objects.all()
		config = ConfigurationReview.objects.all()
	else:
#		total_object = Task.objects.filter(assigned_by__user=request.user)
		app = ApplicationSecurity.objects.filter(task__assigned_by__user=request.user)
		vapt = VaptAssessment.objects.filter(task__assigned_by__user=request.user)
		config = ConfigurationReview.objects.filter(task__assigned_by__user=request.user)

	app_not_assigned = sum(app.filter(task__status__exact='not_assigned'))
	app_in_progress = sum(app.filter(task__status__exact='in_progress'))
	app_rejected = sum(app.filter(task__status__exact='rejected'))
	app_completed = sum(app.filter(task__status__exact='completed'))
	app_total = app_not_assigned + app_in_progress + app_rejected + app_completed

	vapt_not_assigned = sum(vapt.filter(task__status__exact='not_assigned'))
	vapt_in_progress = sum(vapt.filter(task__status__exact='in_progress'))
	vapt_rejected = sum(vapt.filter(task__status__exact='rejected'))
	vapt_completed = sum(vapt.filter(task__status__exact='completed'))
	vapt_total = vapt_not_assigned + vapt_in_progress + vapt_rejected + vapt_completed

	config_not_assigned = sum(config.filter(task__status__exact='not_assigned'))
	config_in_progress = sum(config.filter(task__status__exact='in_progress'))
	config_rejected = sum(config.filter(task__status__exact='rejected'))
	config_completed = sum(config.filter(task__status__exact='completed'))
	config_total = config_not_assigned + config_in_progress + config_rejected + config_completed

	total = app_total + vapt_total + config_total
	not_assigned = app_not_assigned + vapt_not_assigned + config_not_assigned
	in_progress = app_in_progress + vapt_in_progress + config_in_progress 
	rejected = app_rejected + vapt_rejected + config_rejected
	completed = app_completed + vapt_completed + config_completed
		
	context = {
		'total' : total,
		'total_not_assigned' : not_assigned,
		'total_in_progress' : in_progress,
		'total_rejected' : rejected,
		'total_completed' : completed,

		'app_sec' : {
			'total' : app_total,
			'not_assigned' : app_not_assigned,
			'in_progress' : app_in_progress,
			'rejected' : app_rejected,
			'completed' : app_completed,
		},
		
		'vapt' : {
			'total' : vapt_total,
			'not_assigned' : vapt_not_assigned,
			'in_progress' : vapt_in_progress,
			'rejected' : vapt_rejected,
			'completed' : vapt_completed,
		},

		'config' : {
			'total' : config_total,
			'not_assigned' : config_not_assigned,
			'in_progress' : config_in_progress,
			'rejected' : config_rejected,
			'completed' : config_completed,
		},
	}

	return render(request, 'home.html', context=context)

#class appllcationsecurity(LoginRequiredMixin, View):
class ApplicationSecurityListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def query_without_filter(self):
		app = ApplicationSecurity.objects.all().order_by('-task__date_posted')

		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
		
		category = self.request.GET.get('category')
		access = self.request.GET.get('access')
		depart = self.request.GET.get('depart')
		critical = self.request.GET.get('critical')

		if depart:
			app = app.filter(task__assigned_by__department__name__iexact=depart)
		if critical:
			app = app.filter(critical=critical)
		if category:
			app = app.filter(category=category)
		if access:
			app = app.filter(accessibility=access)

		return app

	def get_queryset(self):
		app = self.query_without_filter()

		status = self.request.GET.get('status')
		if status:
			app = app.filter(task__status=status)

		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = self.query_without_filter()
			
		context['not_assigned'] = sum(app.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(app.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(app.filter(task__status__exact="rejected"))
		context['completed'] = sum(app.filter(task__status__exact="completed"))
		context['total'] = sum(app)
		
		title = "Penetration Testing"
		category = self.request.GET.get('category')
		access = self.request.GET.get('access')
		depart = self.request.GET.get('depart')
		critical = self.request.GET.get('critical')

		if category == 'webapp':
			title = title + " - Web Application"
		elif category == 'webservice':
			title = title + " - Web Service"
		elif category == 'mobileapp':
			title = title + " - Mobile Application"

		if access == 'internal':
			title = title + " (Internal)"
		elif access == 'external':
			title = title + " (External)"
			
		if critical == 'y':
			title = title + " (Critical Applications)"

		context['title'] = title
		return context

class WebAppIntListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.filter(category='webapp', accessibility='internal').order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.filter(category='webapp', accessibility='internal')
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing - Web Application (Internal)"
		return context

class WebAppExtListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.filter(category='webapp', accessibility='external').order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.filter(category='webapp', accessibility='external')
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing - Web Application (External)"
		return context

class WebServIntListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.filter(category='webservice', accessibility='internal').order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.filter(category='webservice', accessibility='internal')
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing - Web Service (Internal)"
		return context

class WebServExtListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.filter(category='webservice', accessibility='external').order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.filter(category='webservice', accessibility='external')
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing - Web Service (External)"
		return context

class MobAppListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.filter(category='mobileapp').order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.filter(category='mobileapp')
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing - Mobile Application"
		return context

class VaptAssessmentListView(LoginRequiredMixin, generic.ListView):
	model = VaptAssessment
	context_object_name = 'vapt_assessment_list'
	template_name = 'activities/vaptAssessment.html'
	paginate_by = 15

	def query_without_filter(self):
		vapt = VaptAssessment.objects.all().order_by('-task__date_posted')

		if self.request.user.groups.filter(name="Client").exists():
			vapt = vapt.filter(task__assigned_by__user=self.request.user)
		
		depart = self.request.GET.get('depart')

		if depart:
			vapt = vapt.filter(task__assigned_by__department__name__iexact=depart)

		return vapt

	def get_queryset(self):
		vapt = self.query_without_filter()

		status = self.request.GET.get('status')
		
		if status:
			vapt = vapt.filter(task__status=status)

		return vapt

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		vapt = self.query_without_filter()
		
		if self.request.user.groups.filter(name="Client").exists():
			vapt = vapt.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = sum(vapt)
		context['not_assigned'] = sum(vapt.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(vapt.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(vapt.filter(task__status__exact="rejected"))
		context['completed'] = sum(vapt.filter(task__status__exact="completed"))
		
		return context

class ConfigurationReviewListView(LoginRequiredMixin, generic.ListView):
	model = ConfigurationReview
	context_object_name = 'config_review_list'
	template_name = 'activities/configReview.html'
	paginate_by = 15

	def query_without_filter(self):
		config = ConfigurationReview.objects.all().order_by('-task__date_posted')

		if self.request.user.groups.filter(name="Client").exists():
			config = config.filter(task__assigned_by__user=self.request.user)
		
		depart = self.request.GET.get('depart')

		if depart:
			config = config.filter(task__assigned_by__department__name__iexact=depart)

		return config

	def get_queryset(self):
		config = self.query_without_filter()

		status = self.request.GET.get('status')
		
		if status:
			config = config.filter(task__status=status)
		
		return config

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		config = self.query_without_filter()
		
		if self.request.user.groups.filter(name="Client").exists():
			config = config.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = sum(config)
		context['not_assigned'] = sum(config.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(config.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(config.filter(task__status__exact="rejected"))
		context['completed'] = sum(config.filter(task__status__exact="completed"))

		return context

class BulkActivityListView(LoginRequiredMixin, generic.ListView):
	model = BulkActivity
	context_object_name = 'bulk_activity_list'
	template_name = 'activities/bulkActivity.html'
	paginate_by = 15

	def get_queryset(self):
		bulk = BulkActivity.objects.all().order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return bulk.filter(task__assigned_by__user=self.request.user)
		return bulk

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		bulk = BulkActivity.objects.all()
		
		if self.request.user.groups.filter(name="Client").exists():
			bulk = bulk.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = bulk.count()
		context['not_assigned'] = bulk.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = bulk.filter(task__status__exact="in_progress").count()
		context['rejected'] = bulk.filter(task__status__exact="rejected").count()
		context['completed'] = bulk.filter(task__status__exact="completed").count()

		return context

class ApplicationSecurityDetailView(LoginRequiredMixin, generic.DetailView):
	model = ApplicationSecurity
	context_object_name = 'application_security'
	template_name = 'activities/applicationSecurityDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.all()
		
		activity_task = get_object_or_404(ApplicationSecurity, pk=self.kwargs['pk']).task
		if self.request.user.groups.filter(name="Client").exists():
			if not activity_task.assigned_by.user == self.request.user:
				return None	#TODO: Return proper error 
			app = app.filter(task__assigned_by__user=self.request.user)
		else:
			context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to.pk if activity_task.assigned_to else None})
			
		context['total'] = sum(app)
		context['not_assigned'] = sum(app.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(app.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(app.filter(task__status__exact="rejected"))
		context['completed'] = sum(app.filter(task__status__exact="completed"))

		return context

class VaptAssessmentDetailView(LoginRequiredMixin, generic.DetailView):
	model = VaptAssessment
	context_object_name = 'vapt_assessment_list'
	template_name = 'activities/vaptAssessmentDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		vapt = VaptAssessment.objects.all()
		
		activity_task = get_object_or_404(VaptAssessment, pk=self.kwargs['pk']).task
		if self.request.user.groups.filter(name="Client").exists():
			if not activity_task.assigned_by.user == self.request.user:
				return None 
			vapt = vapt.filter(task__assigned_by__user=self.request.user)
		else:
			context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to.pk if activity_task.assigned_to else None})
			
		context['total'] = sum(vapt)
		context['not_assigned'] = sum(vapt.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(vapt.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(vapt.filter(task__status__exact="rejected"))
		context['completed'] = sum(vapt.filter(task__status__exact="completed"))

		return context

class ConfigurationReviewDetailView(LoginRequiredMixin, generic.DetailView):
	model = ConfigurationReview
	context_object_name = 'config_review_list'
	template_name = 'activities/configReviewDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		config = ConfigurationReview.objects.all()
		
		activity_task = get_object_or_404(ConfigurationReview, pk=self.kwargs['pk']).task
		if self.request.user.groups.filter(name="Client").exists():
			if not activity_task.assigned_by.user == self.request.user:
				return None 
			config = config.filter(task__assigned_by__user=self.request.user)
		else:
			context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to.pk if activity_task.assigned_to else None})
			
		context['total'] = sum(config)
		context['not_assigned'] = sum(config.filter(task__status__exact="not_assigned"))
		context['in_progress'] = sum(config.filter(task__status__exact="in_progress"))
		context['rejected'] = sum(config.filter(task__status__exact="rejected"))
		context['completed'] = sum(config.filter(task__status__exact="completed"))

		return context

#Delete after check
class BulkActivityDetailView(LoginRequiredMixin, generic.DetailView):
	model = BulkActivity
	context_object_name = 'bulk_activity_list'
	template_name = 'activities/BulkActivityDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		bulk = BulkActivity.objects.all()
		
		activity_task = get_object_or_404(BulkActivity, pk=self.kwargs['pk']).task
		if self.request.user.groups.filter(name="Client").exists():
			if not activity_task.assigned_by.user == self.request.user:
				return None 
			bulk = bulk.filter(task__assigned_by__user=self.request.user)
		else:
			context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to.pk if activity_task.assigned_to else None})
			
		context['total'] = bulk.count()
		context['not_assigned'] = bulk.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = bulk.filter(task__status__exact="in_progress").count()
		context['rejected'] = bulk.filter(task__status__exact="rejected").count()
		context['completed'] = bulk.filter(task__status__exact="completed").count()

		return context

@login_required
@permission_required('activities.add_task', raise_exception=True)
def requestApplicationSecurity(request):
	if request.method == 'POST':
		form = RequestApplicationSecurity(request.POST)

		if form.is_valid():
			task = Task(
				assigned_by = get_object_or_404(UserProfile, pk=request.user.user_profile.pk)
			)

			print(form.cleaned_data['testing_type'])
			new_application = ApplicationSecurity(
				task=task,
				name=form.cleaned_data['name'],
				url=form.cleaned_data['url'],
				category=form.cleaned_data['category'],
				accessibility = form.cleaned_data['accessibility'],
				testing_type = form.cleaned_data['testing_type'],
				environment = form.cleaned_data['environment'],
				development = form.cleaned_data['development'],
				critical = form.cleaned_data['critical'],
				functionality=form.cleaned_data['functionality'],
				role_count=form.cleaned_data['role_count'],
				loc=form.cleaned_data['loc'],
				owner=form.cleaned_data['owner'],
				spoc=form.cleaned_data['spoc'],
				comments=form.cleaned_data['comments'],
			)
			task.save()
			new_application.save()
			context = {
				'message_type' : 'alert-success',
				'message_title' : 'Success!',
				'message_body' : 'Penetration Testing requested!',
			}
		else:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Please check your input!',
			}
	else:
		context = {}

	form = RequestApplicationSecurity()
	context.update({
		'form':  form,
	})
	return render(request, 'activities/request_application_security.html', context)

@login_required
@permission_required('activities.add_task', raise_exception=True)
def requestVaptAssessment(request):
	if request.method == 'POST':
		form = RequestVaptAssessment(request.POST)

		if form.is_valid():
			task = Task(
				assigned_by = get_object_or_404(UserProfile, pk=request.user.user_profile.pk),
			)
			new_application = VaptAssessment(
				task=task,
				name=form.cleaned_data['name'],
				ip_address=form.cleaned_data['ip_address'],
				item_count=form.cleaned_data['item_count'],
				accessibility=form.cleaned_data['accessibility'],
				environment = form.cleaned_data['environment'],
				device_type=form.cleaned_data['device_type'],
				owner=form.cleaned_data['owner'],
				spoc=form.cleaned_data['spoc'],
				location = form.cleaned_data['location'],
				comments=form.cleaned_data['comments'],
			)
			task.save()
			new_application.save()
			context = {
				'message_type' : 'alert-success',
				'message_title' : 'Success!',
				'message_body' : 'Vulnerability Assessment requested!',
			}
		else:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Please check your input!',
			}
	else:
		context = {}
	
	form = RequestVaptAssessment()
	context.update({
		'form':  form,
	})
	return render(request, 'activities/request_vapt_assessment.html', context)

@login_required
@permission_required('activities.add_task', raise_exception=True)
def requestConfigReview(request):
	if request.method == 'POST':
		form = RequestConfigReview(request.POST)

		if form.is_valid():
			task = Task(
				assigned_by = get_object_or_404(UserProfile, pk=request.user.user_profile.pk),
			)
			task.save()
			new_application = ConfigurationReview(
				task=task,
				name=form.cleaned_data['name'],
				host_name=form.cleaned_data['host_name'],
				item_count=form.cleaned_data['item_count'],
				device_type=form.cleaned_data['device_type'],
				owner = form.cleaned_data['owner'],
				spoc = form.cleaned_data['spoc'],
				location = form.cleaned_data['location'],
				comments=form.cleaned_data['comments'],
			)

			new_application.save()
			context = {
				'message_type' : 'alert-success',
				'message_title' : 'Success!',
				'message_body' : 'Configuration Audit requested!',
			}
		else:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Please check your input!',
			}
	else:
		context = {}

	form = RequestConfigReview()
	context.update({
		'form': form,
	})

	return render(request, 'activities/request_config_review.html', context)

@login_required
@permission_required('activities.add_task', raise_exception=True)
def activityUpload(request):
	if request.method == 'POST':
		form = ActivityUploadForm(request.POST, request.FILES)

		files = request.FILES['files']
		print(type(files))
		file_type = magic.from_buffer(files.read())
		file_name = str(files)
		file_extension = file_name.split('.')
		valid_extension = ['xlsx', 'xls']
		
		if len(file_extension) > 2:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'File with multiple extension is not allowed!',
			}
		elif not file_extension[1] in valid_extension:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'File with given extension is not allowed!',
			}
		elif not "Microsoft Excel" in file_type:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Invalid file type!',
			}
		elif form.is_valid():
			task = Task(
				assigned_by = get_object_or_404(UserProfile, pk=request.user.user_profile.pk),
			)
			task.save()
			form = BulkActivity(
				task = task,
				category = form.cleaned_data['category'],
				files = files,
			)
			form.save()
			context = {
				'message_type' : 'alert-success',
				'message_title' : 'Success!',
				'message_body' : 'Bulk Activity requested!',
			}
		else:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Please check your input!',
			}
	else:
		context = {}

	form = ActivityUploadForm()
	context.update({
		'form': form,
	})

	return render(request, 'activities/request_bulk_activity.html', context=context)
########################################################################

def updateTaskApplication(request, pk):
	task = get_object_or_404(ApplicationSecurity, pk=pk).task
	if request.method == 'POST':
		form = UpdateTask(request.POST)

		if form.is_valid():
			task.status = form.cleaned_data['status']
			task.assigned_to = get_object_or_404(UserProfile, pk=form.cleaned_data['assigned_to'])
			task.save()

		return HttpResponseRedirect(reverse('application_security_detail', kwargs={'pk':pk }))
#	else:
#		form = UpdateTask(initial={'status': task.status, 'assigned_to': task.assigned_to})
#
#	context = {
#		'form': form,
#		'task': task,
#	}
#
#	return render(request, 'activites/applicationSecurityDetail.html', context)

def updateTaskVapt(request, pk):
	task = get_object_or_404(VaptAssessment, pk=pk).task

	if request.method == 'POST':
		form = UpdateTask(request.POST)

		if form.is_valid():
			task.status = form.cleaned_data['status']
			task.assigned_to = get_object_or_404(UserProfile, pk=form.cleaned_data['assigned_to'])
			task.save()

		return HttpResponseRedirect(reverse('vapt_assessment_detail', kwargs={'pk':pk }))
#	else:
#		form = UpdateTask(initial={'status': task.status, 'assigned_to': task.assigned_to})
#
#	context = {
#		'form': form,
#		'task': task,
#	}
#
#	return render(request, 'activites/applicationSecurityDetail.html', context)

def updateTaskConfig(request, pk):
	task = get_object_or_404(ConfigurationReview, pk=pk).task
	if request.method == 'POST':
		form = UpdateTask(request.POST)

		if form.is_valid():
			task.status = form.cleaned_data['status']
			task.assigned_to = get_object_or_404(UserProfile, pk=form.cleaned_data['assigned_to'])
			task.save()

		return HttpResponseRedirect(reverse('config_review_detail', kwargs={'pk':pk }))
#	else:
#		form = UpdateTask(initial={'status': task.status, 'assigned_to': task.assigned_to})
#
#	context = {
#		'form': form,
#		'task': task,
#	}
#
#	return render(request, 'activites/applicationSecurityDetail.html', context)
