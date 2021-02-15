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

@login_required
#@permission_required('activities.change_task', raise_exception=True)
@group_required('Vendor')
def dashboard(request):
	#MKHO
	vapt_mkho_order = 205
	vapt_mkho_offer = 51
	vapt_mkho_complete = 0
	config_mkho_order = 38
	config_mkho_offer = 10
	config_mkho_complete = 10
	pt_webapp_inter_mkho_order = 55
	pt_webapp_inter_mkho_offer = 11
	pt_webapp_inter_mkho_complete = 9
	pt_webservice_inter_mkho_order = 55
	pt_webservice_inter_mkho_offer = 0
	pt_webservice_inter_mkho_complete = 0
	pt_webapp_intra_mkho_order = 20
	pt_webapp_intra_mkho_offer = 5
	pt_webapp_intra_mkho_complete = 4
	pt_webservice_intra_mkho_order = 0
	pt_webservice_intra_mkho_offer = 0
	pt_webservice_intra_mkho_complete = 0
	pt_mobile_mkho_order = 2
	pt_mobile_mkho_offer = 0
	pt_mobile_mkho_complete = 0
	daily_mkho_order = 1
	daily_mkho_offer = 0
	daily_mkho_complete = 0

	#RHQ
	vapt_rhq_order = 198
	vapt_rhq_offer = 51
	vapt_rhq_complete = 51
	config_rhq_order = 155
	config_rhq_offer = 11
	config_rhq_complete = 10
	pt_webapp_inter_rhq_order = 3
	pt_webapp_inter_rhq_offer = 1
	pt_webapp_inter_rhq_complete = 1
	pt_webservice_inter_rhq_order = 0
	pt_webservice_inter_rhq_offer = 0
	pt_webservice_inter_rhq_complete = 0
	pt_webapp_intra_rhq_order = 95
	pt_webapp_intra_rhq_offer = 10
	pt_webapp_intra_rhq_complete = 10
	pt_webservice_intra_rhq_order = 1
	pt_webservice_intra_rhq_offer = 0
	pt_webservice_intra_rhq_complete = 0
	pt_mobile_rhq_order = 1
	pt_mobile_rhq_offer = 0
	pt_mobile_rhq_complete = 0
	daily_rhq_order = 0
	daily_rhq_offer = 0
	daily_rhq_complete = 0

	#PLHO
	vapt_plho_order = 33
	vapt_plho_offer = 30
	vapt_plho_complete = 0
	config_plho_order = 16
	config_plho_offer = 16
	config_plho_complete = 14
	pt_webapp_inter_plho_order = 5
	pt_webapp_inter_plho_offer = 3
	pt_webapp_inter_plho_complete = 3
	pt_webservice_inter_plho_order = 2
	pt_webservice_inter_plho_offer = 1
	pt_webservice_inter_plho_complete = 1
	pt_webapp_intra_plho_order = 11
	pt_webapp_intra_plho_offer = 2
	pt_webapp_intra_plho_complete = 1
	pt_webservice_intra_plho_order = 0
	pt_webservice_intra_plho_offer = 0
	pt_webservice_intra_plho_complete = 0
	pt_mobile_plho_order = 3
	pt_mobile_plho_offer = 1
	pt_mobile_plho_complete = 1
	daily_plho_order = 0
	daily_plho_offer = 0
	daily_plho_complete = 0
	
	#RD
	vapt_rd_order = 40
	vapt_rd_offer = 40
	vapt_rd_complete = 40
	config_rd_order = 8
	config_rd_offer = 7
	config_rd_complete = 7
	pt_webapp_inter_rd_order = 0
	pt_webapp_inter_rd_offer = 0
	pt_webapp_inter_rd_complete = 0
	pt_webservice_inter_rd_order = 0
	pt_webservice_inter_rd_offer = 0
	pt_webservice_inter_rd_complete = 0
	pt_webapp_intra_rd_order = 5
	pt_webapp_intra_rd_offer = 5
	pt_webapp_intra_rd_complete = 5
	pt_webapp_intra_bd_order = 0
	pt_webapp_intra_bd_offer = 0
	pt_webapp_intra_bd_complete = 0
	pt_webservice_intra_rd_order = 0
	pt_webservice_intra_rd_offer = 0
	pt_webservice_intra_rd_complete = 0
	pt_mobile_rd_order = 0
	pt_mobile_rd_offer = 0
	pt_mobile_rd_complete = 0
	daily_rd_order = 0
	daily_rd_offer = 0
	daily_rd_complete = 0
	
	#BD
	vapt_bd_order = 14
	vapt_bd_offer = 14
	vapt_bd_complete = 14
	config_bd_order = 0
	config_bd_offer = 0
	config_bd_complete = 0
	pt_webapp_inter_bd_order = 3
	pt_webapp_inter_bd_offer = 3
	pt_webapp_inter_bd_complete = 3
	pt_webservice_inter_bd_order = 0
	pt_webservice_inter_bd_offer = 0
	pt_webservice_inter_bd_complete = 0
	pt_webservice_intra_bd_order = 0
	pt_webservice_intra_bd_offer = 0
	pt_webservice_intra_bd_complete = 0
	pt_mobile_bd_order = 0
	pt_mobile_bd_offer = 0
	pt_mobile_bd_complete = 0
	daily_bd_order = 0
	daily_bd_offer = 0
	daily_bd_complete = 0
	
	#COIS
	vapt_cois_order = 495
	vapt_cois_offer = 173
	vapt_cois_complete = 173
	config_cois_order = 89
	config_cois_offer = 0
	config_cois_complete = 0
	pt_webapp_inter_cois_order = 13
	pt_webapp_inter_cois_offer = 6
	pt_webapp_inter_cois_complete = 4
	pt_webservice_inter_cois_order = 82
	pt_webservice_inter_cois_offer = 0
	pt_webservice_inter_cois_complete = 0
	pt_webapp_intra_cois_order = 31
	pt_webapp_intra_cois_offer = 5
	pt_webapp_intra_cois_complete = 3
	pt_webservice_intra_cois_order = 13
	pt_webservice_intra_cois_offer = 4
	pt_webservice_intra_cois_complete = 0
	pt_mobile_cois_order = 7
	pt_mobile_cois_offer = 0
	pt_mobile_cois_complete = 0
	daily_cois_order = 3
	daily_cois_offer = 0
	daily_cois_complete = 0

	#Department wise total
	mkho_order = vapt_mkho_order + config_mkho_order + pt_webapp_inter_mkho_order + pt_webservice_inter_mkho_order + pt_webapp_intra_mkho_order + pt_webservice_intra_mkho_order + pt_mobile_mkho_order + daily_mkho_order
	mkho_offer = vapt_mkho_offer + config_mkho_offer + pt_webapp_inter_mkho_offer + pt_webservice_inter_mkho_offer + pt_webapp_intra_mkho_offer + pt_webservice_intra_mkho_offer + pt_mobile_mkho_offer + daily_mkho_offer
	mkho_complete = vapt_mkho_complete + config_mkho_complete + pt_webapp_inter_mkho_complete + pt_webservice_inter_mkho_complete + pt_webapp_intra_mkho_complete + pt_webservice_intra_mkho_complete + pt_mobile_mkho_complete + daily_mkho_complete

	rhq_order = vapt_rhq_order + config_rhq_order + pt_webapp_inter_rhq_order + pt_webservice_inter_rhq_order + pt_webapp_intra_rhq_order + pt_webservice_intra_rhq_order + pt_mobile_rhq_order + daily_rhq_order
	rhq_offer = vapt_rhq_offer + config_rhq_offer + pt_webapp_inter_rhq_offer + pt_webservice_inter_rhq_offer + pt_webapp_intra_rhq_offer + pt_webservice_intra_rhq_offer + pt_mobile_rhq_offer + daily_rhq_offer
	rhq_complete = vapt_rhq_complete + config_rhq_complete + pt_webapp_inter_rhq_complete + pt_webservice_inter_rhq_complete + pt_webapp_intra_rhq_complete + pt_webservice_intra_rhq_complete + pt_mobile_rhq_complete + daily_rhq_complete

	plho_order = vapt_plho_order + config_plho_order + pt_webapp_inter_plho_order + pt_webservice_inter_plho_order + pt_webapp_intra_plho_order + pt_webservice_intra_plho_order + pt_mobile_plho_order + daily_plho_order
	plho_offer = vapt_plho_offer + config_plho_offer + pt_webapp_inter_plho_offer + pt_webservice_inter_plho_offer + pt_webapp_intra_plho_offer + pt_webservice_intra_plho_offer + pt_mobile_plho_offer + daily_plho_offer
	plho_complete = vapt_plho_complete + config_plho_complete + pt_webapp_inter_plho_complete + pt_webservice_inter_plho_complete + pt_webapp_intra_plho_complete + pt_webservice_intra_plho_complete + pt_mobile_plho_complete + daily_plho_complete

	rd_order = vapt_rd_order + config_rd_order + pt_webapp_inter_rd_order + pt_webservice_inter_rd_order + pt_webapp_intra_rd_order + pt_webservice_intra_rd_order + pt_mobile_rd_order + daily_rd_order
	rd_offer = vapt_rd_offer + config_rd_offer + pt_webapp_inter_rd_offer + pt_webservice_inter_rd_offer + pt_webapp_intra_rd_offer + pt_webservice_intra_rd_offer + pt_mobile_rd_offer + daily_rd_offer
	rd_complete = vapt_rd_complete + config_rd_complete + pt_webapp_inter_rd_complete + pt_webservice_inter_rd_complete + pt_webapp_intra_rd_complete + pt_webservice_intra_rd_complete + pt_mobile_rd_complete + daily_rd_complete

	bd_order = vapt_bd_order + config_bd_order + pt_webapp_inter_bd_order + pt_webservice_inter_bd_order + pt_webapp_intra_bd_order + pt_webservice_intra_bd_order + pt_mobile_bd_order + daily_bd_order
	bd_offer = vapt_bd_offer + config_bd_offer + pt_webapp_inter_bd_offer + pt_webservice_inter_bd_offer + pt_webapp_intra_bd_offer + pt_webservice_intra_bd_offer + pt_mobile_bd_offer + daily_bd_offer
	bd_complete = vapt_bd_complete + config_bd_complete + pt_webapp_inter_bd_complete + pt_webservice_inter_bd_complete + pt_webapp_intra_bd_complete + pt_webservice_intra_bd_complete + pt_mobile_bd_complete + daily_bd_complete

	cois_order = vapt_cois_order + config_cois_order + pt_webapp_inter_cois_order + pt_webservice_inter_cois_order + pt_webapp_intra_cois_order + pt_webservice_intra_cois_order + pt_mobile_cois_order + daily_cois_order
	cois_offer = vapt_cois_offer + config_cois_offer + pt_webapp_inter_cois_offer + pt_webservice_inter_cois_offer + pt_webapp_intra_cois_offer + pt_webservice_intra_cois_offer + pt_mobile_cois_offer + daily_cois_offer
	cois_complete = vapt_cois_complete + config_cois_complete + pt_webapp_inter_cois_complete + pt_webservice_inter_cois_complete + pt_webapp_intra_cois_complete + pt_webservice_intra_cois_complete + pt_mobile_cois_complete + daily_cois_complete

	#Total
	total = mkho_order + rhq_order + plho_order + rd_order + bd_order + cois_order
	total_rejected = 0
	total_not_assigned = 0
	total_completed =  mkho_complete + rhq_complete + plho_complete + rd_complete + bd_complete + cois_complete
	total_in_progress = total - total_completed - total_rejected - total_not_assigned 

	context = {
		'total' : total,
		'total_not_assigned' : total_not_assigned,
		'total_in_progress' : total_in_progress,
		'total_rejected' : total_rejected,
		'total_completed' : total_completed,
		'vapt': {
			'mkho': {
				'order': vapt_mkho_order,
				'offer': vapt_mkho_offer,
				'complete': vapt_mkho_complete,
			},
			'rhq': {
				'order': vapt_rhq_order,
				'offer': vapt_rhq_offer,
				'complete': vapt_rhq_complete,
			},
			'plho': {
				'order': vapt_plho_order,
				'offer': vapt_plho_offer,
				'complete': vapt_plho_complete,
			},
			'rd': {
				'order': vapt_rd_order,
				'offer': vapt_rd_offer,
				'complete': vapt_rd_complete,
			},
			'bd': {
				'order': vapt_bd_order,
				'offer': vapt_bd_offer,
				'complete': vapt_bd_complete,
			},
			'cois': {
				'order': vapt_cois_order,
				'offer': vapt_cois_offer,
				'complete': vapt_cois_complete,
			},
		},
		'config': {
			'mkho': {
				'order': config_mkho_order,
				'offer': config_mkho_offer,
				'complete': config_mkho_complete,
			},
			'rhq': {
				'order': config_rhq_order,
				'offer': config_rhq_offer,
				'complete': config_rhq_complete,
			},
			'plho': {
				'order': config_plho_order,
				'offer': config_plho_offer,
				'complete': config_plho_complete,
			},
			'rd': {
				'order': config_rd_order,
				'offer': config_rd_offer,
				'complete': config_rd_complete,
			},
			'bd': {
				'order': config_bd_order,
				'offer': config_bd_offer,
				'complete': config_bd_complete,
			},
			'cois': {
				'order': config_cois_order,
				'offer': config_cois_offer,
				'complete': config_cois_complete,
			},
		},
		'pt': {
			'webapp': {
				'inter': {
					'mkho': {
						'order': pt_webapp_inter_mkho_order,
						'offer': pt_webapp_inter_mkho_offer,
						'complete': pt_webapp_inter_mkho_complete,
					},
					'rhq': {
						'order': pt_webapp_inter_rhq_order,
						'offer': pt_webapp_inter_rhq_offer,
						'complete': pt_webapp_inter_rhq_complete,
					},
					'plho': {
						'order': pt_webapp_inter_plho_order,
						'offer': pt_webapp_inter_plho_offer,
						'complete': pt_webapp_inter_plho_complete,
					},
					'rd': {
						'order': pt_webapp_inter_rd_order,
						'offer': pt_webapp_inter_rd_offer,
						'complete': pt_webapp_inter_rd_complete,
					},
					'bd': {
						'order': pt_webapp_inter_bd_order,
						'offer': pt_webapp_inter_bd_offer,
						'complete': pt_webapp_inter_bd_complete,
					},
					'cois': {
						'order': pt_webapp_inter_cois_order,
						'offer': pt_webapp_inter_cois_offer,
						'complete': pt_webapp_inter_cois_complete,
					},
				},
				'intra': {
					'mkho': {
						'order': pt_webapp_intra_mkho_order,
						'offer': pt_webapp_intra_mkho_offer,
						'complete': pt_webapp_intra_mkho_complete,
					},
					'rhq': {
						'order': pt_webapp_intra_rhq_order,
						'offer': pt_webapp_intra_rhq_offer,
						'complete': pt_webapp_intra_rhq_complete,
					},
					'plho': {
						'order': pt_webapp_intra_plho_order,
						'offer': pt_webapp_intra_plho_offer,
						'complete': pt_webapp_intra_plho_complete,
					},
					'rd': {
						'order': pt_webapp_intra_rd_order,
						'offer': pt_webapp_intra_rd_offer,
						'complete': pt_webapp_intra_rd_complete,
					},
					'bd': {
						'order': pt_webapp_intra_bd_order,
						'offer': pt_webapp_intra_bd_offer,
						'complete': pt_webapp_intra_bd_complete,
					},
					'cois': {
						'order': pt_webapp_intra_cois_order,
						'offer': pt_webapp_intra_cois_offer,
						'complete': pt_webapp_intra_cois_complete,
					},
				},
			},
			'webservice': {
				'inter': {
					'mkho': {
						'order': pt_webservice_inter_mkho_order,
						'offer': pt_webservice_inter_mkho_offer,
						'complete': pt_webservice_inter_mkho_complete,
					},
					'rhq': {
						'order': pt_webservice_inter_rhq_order,
						'offer': pt_webservice_inter_rhq_offer,
						'complete': pt_webservice_inter_rhq_complete,
					},
					'plho': {
						'order': pt_webservice_inter_plho_order,
						'offer': pt_webservice_inter_plho_offer,
						'complete': pt_webservice_inter_plho_complete,
					},
					'rd': {
						'order': pt_webservice_inter_rd_order,
						'offer': pt_webservice_inter_rd_offer,
						'complete': pt_webservice_inter_rd_complete,
					},
					'bd': {
						'order': pt_webservice_inter_bd_order,
						'offer': pt_webservice_inter_bd_offer,
						'complete': pt_webservice_inter_bd_complete,
					},
					'cois': {
						'order': pt_webservice_inter_bd_order,
						'offer': pt_webservice_inter_bd_offer,
						'complete': pt_webservice_inter_bd_complete,
					},
				},
				'intra': {
					'mkho': {
						'order': pt_webservice_intra_mkho_order,
						'offer': pt_webservice_intra_mkho_offer,
						'complete': pt_webservice_intra_mkho_complete,
					},
					'rhq': {
						'order': pt_webservice_intra_rhq_order,
						'offer': pt_webservice_intra_rhq_offer,
						'complete': pt_webservice_intra_rhq_complete,
					},
					'plho': {
						'order': pt_webservice_intra_plho_order,
						'offer': pt_webservice_intra_plho_offer,
						'complete': pt_webservice_intra_plho_complete,
					},
					'rd': {
						'order': pt_webservice_intra_rd_order,
						'offer': pt_webservice_intra_rd_offer,
						'complete': pt_webservice_intra_rd_complete,
					},
					'bd': {
						'order': pt_webservice_intra_bd_order,
						'offer': pt_webservice_intra_bd_offer,
						'complete': pt_webservice_intra_bd_complete,
					},
					'cois': {
						'order': pt_webservice_intra_cois_order,
						'offer': pt_webservice_intra_cois_offer,
						'complete': pt_webservice_intra_cois_complete,
					},
				},
			},
			'mobile': {
				'mkho': {
					'order': pt_mobile_mkho_order,
					'offer': pt_mobile_mkho_offer,
					'complete': pt_mobile_mkho_complete,
				},
				'rhq': {
					'order': pt_mobile_rhq_order,
					'offer': pt_mobile_rhq_offer,
					'complete': pt_mobile_rhq_complete,
				},
				'plho': {
					'order': pt_mobile_plho_order,
					'offer': pt_mobile_plho_offer,
					'complete': pt_mobile_plho_complete,
				},
				'rd': {
					'order': pt_mobile_rd_order,
					'offer': pt_mobile_rd_offer,
					'complete': pt_mobile_rd_complete,
				},
				'bd': {
					'order': pt_mobile_bd_order,
					'offer': pt_mobile_bd_offer,
					'complete': pt_mobile_bd_complete,
				},
				'cois': {
					'order': pt_mobile_cois_order,
					'offer': pt_mobile_cois_offer,
					'complete': pt_mobile_cois_complete,
				},
			},
		},
		'daily': {
			'mkho': {
				'order': daily_mkho_order,
				'offer': daily_mkho_offer,
				'complete': daily_mkho_complete,
			},
			'rhq': {
				'order': daily_rhq_order,
				'offer': daily_rhq_offer,
				'complete': daily_rhq_complete,
			},
			'plho': {
				'order': daily_plho_order,
				'offer': daily_plho_offer,
				'complete': daily_plho_complete,
			},
			'rd': {
				'order': daily_rd_order,
				'offer': daily_rd_offer,
				'complete': daily_rd_complete,
			},
			'bd': {
				'order': daily_bd_order,
				'offer': daily_bd_offer,
				'complete': daily_bd_complete,
			},
			'cois': {
				'order': daily_cois_order,
				'offer': daily_cois_offer,
				'complete': daily_cois_complete,
			},
		},
	}
	return render(request, 'dashboard.html', context=context)

@login_required
@permission_required('activities.change_task', raise_exception=True)
def department(request):
	app = ApplicationSecurity.objects.all()
	vapt = VaptAssessment.objects.all()
	config = ConfigurationReview.objects.all()
	
	depart = request.GET.get('depart')

	if depart:
		print(depart)
		app = app.filter(task__assigned_by__department__name__iexact=depart)
		vapt = vapt.filter(task__assigned_by__department__name__iexact=depart)
		config = config.filter(task__assigned_by__department__name__iexact=depart)

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

	return render(request, 'department.html', context=context)
