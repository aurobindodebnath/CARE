from django.shortcuts import render, get_object_or_404
from activities.models import * 
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from activities.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def index(request):
	total = Task.objects.all().count()
	not_assigned = Task.objects.filter(status__exact='not_assigned').count()
	in_progress = Task.objects.filter(status__exact='in_progress').count()
	rejected = Task.objects.filter(status__exact='rejected').count()
	completed = Task.objects.filter(status__exact='completed').count()

	app_total = ApplicationSecurity.objects.all().count()
	app_not_assigned = ApplicationSecurity.objects.filter(task__status__exact='not_assigned').count()
	app_in_progress = ApplicationSecurity.objects.filter(task__status__exact='in_progress').count()
	app_rejected = ApplicationSecurity.objects.filter(task__status__exact='rejected').count()
	app_completed = ApplicationSecurity.objects.filter(task__status__exact='completed').count()

	vapt_total = VaptAssessment.objects.all().count()
	vapt_not_assigned = VaptAssessment.objects.filter(task__status__exact='not_assigned').count()
	vapt_in_progress = VaptAssessment.objects.filter(task__status__exact='in_progress').count()
	vapt_rejected = VaptAssessment.objects.filter(task__status__exact='rejected').count()
	vapt_completed = VaptAssessment.objects.filter(task__status__exact='completed').count()


	config_total = ConfigurationReview.objects.all().count()
	config_not_assigned = ConfigurationReview.objects.filter(task__status__exact='not_assigned').count()
	config_in_progress = ConfigurationReview.objects.filter(task__status__exact='in_progress').count()
	config_rejected = ConfigurationReview.objects.filter(task__status__exact='rejected').count()
	config_completed = ConfigurationReview.objects.filter(task__status__exact='completed').count()


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
	queryset = ApplicationSecurity.objects.all()[:5]
	template_name = 'activities/applicationSecurity.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = ApplicationSecurity.objects.all().count()
		context['not_assigned'] = ApplicationSecurity.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = ApplicationSecurity.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = ApplicationSecurity.objects.filter(task__status__exact="rejected").count()
		context['completed'] = ApplicationSecurity.objects.filter(task__status__exact="completed").count()
		return context

class VaptAssessmentListView(LoginRequiredMixin, generic.ListView):
	model = VaptAssessment
	context_object_name = 'vapt_assessment_list'
	queryset = VaptAssessment.objects.all()[:5]
	template_name = 'activities/vaptAssessment.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = VaptAssessment.objects.all().count()
		context['not_assigned'] = VaptAssessment.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = VaptAssessment.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = VaptAssessment.objects.filter(task__status__exact="rejected").count()
		context['completed'] = VaptAssessment.objects.filter(task__status__exact="completed").count()
		return context

class ConfigurationReviewListView(LoginRequiredMixin, generic.ListView):
	model = ConfigurationReview
	context_object_name = 'config_review_list'
	ordering = ['-task__date_posted',]
	queryset = ConfigurationReview.objects.all()
	template_name = 'activities/configReview.html'
	#TODO: use pagination
	#TODO: use get_queryset for filtering
	#paginate_by = 1

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['total'] = ConfigurationReview.objects.all().count()
		context['not_assigned'] = ConfigurationReview.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = ConfigurationReview.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = ConfigurationReview.objects.filter(task__status__exact="rejected").count()
		context['completed'] = ConfigurationReview.objects.filter(task__status__exact="completed").count()
		return context

class ApplicationSecurityDetailView(LoginRequiredMixin, generic.DetailView):
	model = ApplicationSecurity
	context_object_name = 'application_security'
	template_name = 'activities/applicationSecurityDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		activity_task = get_object_or_404(ApplicationSecurity, pk=self.kwargs['pk']).task
		context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to})
		context['total'] = ApplicationSecurity.objects.all().count()
		context['not_assigned'] = ApplicationSecurity.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = ApplicationSecurity.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = ApplicationSecurity.objects.filter(task__status__exact="rejected").count()
		context['completed'] = ApplicationSecurity.objects.filter(task__status__exact="completed").count()
		return context

class VaptAssessmentDetailView(LoginRequiredMixin, generic.DetailView):
	model = VaptAssessment
	context_object_name = 'vapt_assessment_list'
	template_name = 'activities/vaptAssessmentDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		activity_task = get_object_or_404(VaptAssessment, pk=self.kwargs['pk']).task
		context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to})
		context['total'] = VaptAssessment.objects.all().count()
		context['not_assigned'] = VaptAssessment.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = VaptAssessment.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = VaptAssessment.objects.filter(task__status__exact="rejected").count()
		context['completed'] = VaptAssessment.objects.filter(task__status__exact="completed").count()
		return context

class ConfigurationReviewDetailView(LoginRequiredMixin, generic.DetailView):
	model = ConfigurationReview
	context_object_name = 'config_review_list'
	template_name = 'activities/configReviewDetail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		activity_task = get_object_or_404(ConfigurationReview, pk=self.kwargs['pk']).task
		context['form'] = UpdateTask(initial={'status': activity_task.status, 'assigned_to': activity_task.assigned_to})
		context['total'] = ConfigurationReview.objects.all().count()
		context['not_assigned'] = ConfigurationReview.objects.filter(task__status__exact="not_assigned").count()
		context['in_progress'] = ConfigurationReview.objects.filter(task__status__exact="in_progress").count()
		context['rejected'] = ConfigurationReview.objects.filter(task__status__exact="rejected").count()
		context['completed'] = ConfigurationReview.objects.filter(task__status__exact="completed").count()
		return context

@login_required
def requestApplicationSecurity(request):
	if request.method == 'POST':
		form = RequestApplicationSecurity(request.POST)

		if form.is_valid():
			task = Task(
				code=form.cleaned_data['task_code'],
				assigned_by = get_object_or_404(User, pk=request.user.pk).user_profile,
			)
			task.save()
			new_application = ApplicationSecurity(
				task=task,
				name=form.cleaned_data['name'],
				url=form.cleaned_data['url'],
				functionality=form.cleaned_data['functionality'],
				business_purpose=form.cleaned_data['business_purpose'],
				role_count=form.cleaned_data['role_count'],
				loc=form.cleaned_data['loc'],
				host_server=form.cleaned_data['host_server'],
				frontend_technologies=form.cleaned_data['frontend_technologies'],
				backend_technologies=form.cleaned_data['backend_technologies'],
				credentials=form.cleaned_data['credentials'],
				comments=form.cleaned_data['comments'],
			)

			new_application.save()
			return HttpResponseRedirect(reverse('index'))

	else:
		form = RequestApplicationSecurity()

	context = {
		'form':  form,
	}

	return render(request, 'activities/request_application_security.html', context)

@login_required
def requestVaptAssessment(request):
	if request.method == 'POST':
		form = RequestVaptAssessment(request.POST)

		if form.is_valid():
			task = Task(
				code=form.cleaned_data['task_code'],
				assigned_by = get_object_or_404(User, pk=request.user.pk).user_profile,
			)
			task.save()
			new_application = VaptAssessment(
				task=task,
				name=form.cleaned_data['name'],
				ip_address=form.cleaned_data['ip'],
				device_type=form.cleaned_data['device_type'],
				comments=form.cleaned_data['comments'],
			)

			new_application.save()
			return HttpResponseRedirect(reverse('index'))

	else:
		form = RequestVaptAssessment()

	context = {
		'form':  form,
	}

	return render(request, 'activities/request_vapt_assessment.html', context)

@login_required
def requestConfigReview(request):
	if request.method == 'POST':
		form = RequestConfigReview(request.POST)

		if form.is_valid():
			task = Task(
				code=form.cleaned_data['task_code'],
				assigned_by = get_object_or_404(User, pk=request.user.pk).user_profile,
			)
			task.save()
			new_application = ConfigurationReview(
				task=task,
				name=form.cleaned_data['name'],
				device_type=form.cleaned_data['device_type'],
				host_count=form.cleaned_data['host_count'],
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
