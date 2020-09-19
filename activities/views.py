from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile, ApplicationSecurity, VAPTAssessment, ConfigurationReview

#from .forms import SolutionForm
from django.template.context_processors import csrf

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('loggedin')
	else: 
		return render(request, 'index.html', {})


def login_view(request):
	try:
		username =request.POST['username']
		password= request.POST['password']
		user = authenticate(username=username, password=password)
	except KeyError:
		return render(request, 'index.html',{'login_message' : 'Fill in all fields',}) 
	if user is not None:
		if user.is_active:
			login(request,user)
			return redirect('loggedin')
		else:
			return render(request, 'index.html',{'login_message' : 'The user has been removed',})
	else:
		return render(request, 'index.html',{'login_message' : 'Enter Correct Details',})

@login_required
def loggedin(request):
    appsec_completed = len(ApplicationSecurity.objects.filter(status='Completed'))
    appsec_in_progress = len(ApplicationSecurity.objects.filter(status='In Progress'))
    appsec_rejected = len(ApplicationSecurity.objects.filter(status='Rejected'))
    appsec_unassigned = len(ApplicationSecurity.objects.filter(status='Not Assigned'))
    appsec_requested = appsec_completed + appsec_in_progress + appsec_rejected + appsec_unassigned
    c = {"user": request.user,
        "appsec": {"requested": appsec_requested, "completed": appsec_completed, "in_progress": appsec_in_progress, "not_assigned": appsec_unassigned, "rejected":appsec_rejected,},
        "vapt": {"requested": 8, "completed": 3, "in_progress": 2, "not_assigned": 3, "rejected":0,},
        "config": {"requested": 9, "completed": 3, "in_progress": 3, "not_assigned": 2, "rejected":1,},
        }
    return render(request, 'dash.html', c)

@login_required	
def logout_view(request):
	logout(request)
	return redirect('index')

@login_required
def appsec(request):
    # TO DO
    c = {"user": request.user,
        }
    return render(request, 'appsec.html', c)

@login_required
def vapt(request):
    # TO DO
    c = {"user": request.user,
        }
    return render(request, 'vapt.html', c)

@login_required
def config(request):
    # TO DO
    c = {"user": request.user,
        }
    return render(request, 'config.html', c)

@login_required
def activities(request):
    appsec = ApplicationSecurity.objects.all().order_by('-date_posted')
    vapt = VAPTAssessment.objects.all().order_by('-date_posted')
    config = ConfigurationReview.objects.all().order_by('-date_posted')
    c = {"user": request.user,
        "appsec": appsec,
        "vapt": vapt,
        "config": config,
        }
    return render(request, 'activities.html', c)


@login_required
def appsecDetail(request, unique_id):
    appsec_object = ApplicationSecurity.objects.get(pk=unique_id)
    if request.user.user_profile.organization.role == 'Vender':
        c = {"user": request.user, "object": appsec_object}
        return render(request, 'appsecDetailVendor.html', c)
    else:
        c = {"user": request.user, "object": appsec_object}
        return render(request, 'appsecDetailClient.html', c)