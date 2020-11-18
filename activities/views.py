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
			return HttpResponseRedirect(reverse('index'))
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
def index(request):

	if request.user.groups.filter(name="Vendor").exists():
		total_object = Task.objects.all()
		app = ApplicationSecurity.objects.all()
		vapt = VaptAssessment.objects.all()
		config = ConfigurationReview.objects.all()
	else:
		total_object = Task.objects.filter(assigned_by__user=request.user)
		app = ApplicationSecurity.objects.filter(task__assigned_by__user=request.user)
		vapt = VaptAssessment.objects.filter(task__assigned_by__user=request.user)
		config = ConfigurationReview.objects.filter(task__assigned_by__user=request.user)

	total = total_object.count()
	not_assigned = total_object.filter(status__exact='not_assigned').count()
	in_progress = total_object.filter(status__exact='in_progress').count()
	rejected = total_object.filter(status__exact='rejected').count()
	completed = total_object.filter(status__exact='completed').count()
		
	app_total = app.count()
	app_not_assigned = app.filter(task__status__exact='not_assigned').count()
	app_in_progress = app.filter(task__status__exact='in_progress').count()
	app_rejected = app.filter(task__status__exact='rejected').count()
	app_completed = app.filter(task__status__exact='completed').count()

	vapt_total = vapt.count()
	vapt_not_assigned = vapt.filter(task__status__exact='not_assigned').count()
	vapt_in_progress = vapt.filter(task__status__exact='in_progress').count()
	vapt_rejected = vapt.filter(task__status__exact='rejected').count()
	vapt_completed = vapt.filter(task__status__exact='completed').count()

	config_total = config.count()
	config_not_assigned = config.filter(task__status__exact='not_assigned').count()
	config_in_progress = config.filter(task__status__exact='in_progress').count()
	config_rejected = config.filter(task__status__exact='rejected').count()
	config_completed = config.filter(task__status__exact='completed').count()
		
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

	return render(request, 'index.html', context=context)


#class appllcationsecurity(LoginRequiredMixin, View):
class ApplicationSecurityListView(LoginRequiredMixin, generic.ListView):
	model = ApplicationSecurity
	context_object_name = 'application_security_list'
	template_name = 'activities/applicationSecurity.html'
	paginate_by = 15

	def get_queryset(self):
		app = ApplicationSecurity.objects.all().order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return app.filter(task__assigned_by__user=self.request.user)
		return app

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		app = ApplicationSecurity.objects.all()
		
		if self.request.user.groups.filter(name="Client").exists():
			app = app.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()
		
		context['title'] = "Penetration Testing"
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

	def get_queryset(self):
		vapt = VaptAssessment.objects.all().order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return vapt.filter(task__assigned_by__user=self.request.user)
		return vapt

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		vapt = VaptAssessment.objects.all()
		
		if self.request.user.groups.filter(name="Client").exists():
			vapt = vapt.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = vapt.count()
		context['not_assigned'] = vapt.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = vapt.filter(task__status__exact="in_progress").count()
		context['rejected'] = vapt.filter(task__status__exact="rejected").count()
		context['completed'] = vapt.filter(task__status__exact="completed").count()
		
		return context

class ConfigurationReviewListView(LoginRequiredMixin, generic.ListView):
	model = ConfigurationReview
	context_object_name = 'config_review_list'
	template_name = 'activities/configReview.html'
	paginate_by = 15

	def get_queryset(self):
		config = ConfigurationReview.objects.all().order_by('-task__date_posted')
		if self.request.user.groups.filter(name="Client").exists():
			return config.filter(task__assigned_by__user=self.request.user)
		return config

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		config = ConfigurationReview.objects.all()
		
		if self.request.user.groups.filter(name="Client").exists():
			config = config.filter(task__assigned_by__user=self.request.user)
			
		context['total'] = config.count()
		context['not_assigned'] = config.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = config.filter(task__status__exact="in_progress").count()
		context['rejected'] = config.filter(task__status__exact="rejected").count()
		context['completed'] = config.filter(task__status__exact="completed").count()

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
				return None 
			app = app.filter(task__assigned_by__user=self.request.user)
		else:
			context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to.pk if activity_task.assigned_to else None})
			
		context['total'] = app.count()
		context['not_assigned'] = app.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = app.filter(task__status__exact="in_progress").count()
		context['rejected'] = app.filter(task__status__exact="rejected").count()
		context['completed'] = app.filter(task__status__exact="completed").count()

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
			
		context['total'] = vapt.count()
		context['not_assigned'] = vapt.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = vapt.filter(task__status__exact="in_progress").count()
		context['rejected'] = vapt.filter(task__status__exact="rejected").count()
		context['completed'] = vapt.filter(task__status__exact="completed").count()

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
			
		context['total'] = config.count()
		context['not_assigned'] = config.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = config.filter(task__status__exact="in_progress").count()
		context['rejected'] = config.filter(task__status__exact="rejected").count()
		context['completed'] = config.filter(task__status__exact="completed").count()

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
			print(form.cleaned_data['category'])

			new_application = ApplicationSecurity(
				task=task,
				name=form.cleaned_data['name'],
				category=form.cleaned_data['category'],
				owner=form.cleaned_data['owner'],
				spoc=form.cleaned_data['spoc'],
				url=form.cleaned_data['url'],
				testing_type = form.cleaned_data['testing_type'],
				accessibility = form.cleaned_data['accessibility'],
				development = form.cleaned_data['development'],
				environment = form.cleaned_data['environment'],
				functionality=form.cleaned_data['functionality'],
			#	page_count = form.cleaned_data['page_count'],
				role_count=form.cleaned_data['role_count'],
				loc=form.cleaned_data['loc'],
				comments=form.cleaned_data['comments'],
			)
			task.save()
			new_application.save()
			return HttpResponseRedirect(reverse('index'))

	else:
		form = RequestApplicationSecurity()

	context = {
		'form':  form,
	}
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
				ip_address=form.cleaned_data['ip_address'],
				accessibility=form.cleaned_data['accessibility'],
				owner=form.cleaned_data['owner'],
				spoc=form.cleaned_data['spoc'],
				device_type=form.cleaned_data['device_type'],
				environment = form.cleaned_data['environment'],
				location = form.cleaned_data['files'],
				comments=form.cleaned_data['comments'],
			)
			task.save()
			new_application.save()
			return HttpResponseRedirect(reverse('index'))

	else:
		form = RequestVaptAssessment()

	context = {
		'form':  form,
	}
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
				device_type=form.cleaned_data['device_type'],
				ip_address = form.cleaned_data['ip_address'],
				owner = form.cleaned_data['owner'],
				spoc = form.cleaned_data['spoc'],
				host_count=form.cleaned_data['host_count'],
				location = form.cleaned_data['location'],
				comments=form.cleaned_data['comments'],
			)

			new_application.save()
			return HttpResponseRedirect(reverse('index'))

	else:
		form = RequestConfigReview()

	context = {
		'form':  form,
	}

	return render(request, 'activities/request_config_review.html', context)

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
			task.assigned_to = get_object_or_404(User, pk=form.cleaned_data['assigned_to'])
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
			task.assigned_to = get_object_or_404(User, pk=form.cleaned_data['assigned_to'])
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

@login_required
@permission_required('activities.add_task', raise_exception=True)
def activityUpload(request):
	if request.method == 'POST':
		form = ActivityUploadForm(request.POST, request.FILES)
		files = request.FILES['files']
		file_type = magic.from_buffer(files.read())
		if not "Microsoft Excel" in file_type:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Invalid file type.',
			}
		elif form.is_valid():
			form.save()
			context = {
				'message_type' : 'alert-success',
				'message_title' : 'Success!',
				'message_body' : 'Bulk activity requested.',
			}
		else:
			context = {
				'message_type' : 'alert-danger',
				'message_title' : 'Error!',
				'message_body' : 'Invalid form.',
			}

	form = ActivityUploadForm()
	context.update({
		'form': form,
	})

	return render(request, 'activities/activity_upload.html', context=context)
