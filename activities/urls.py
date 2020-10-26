from django.urls import path, include
from activities import views

urlpatterns = [
	path('', views.index, name='index'),

	path('application_security/', views.ApplicationSecurityListView.as_view(), name='application_security'),
	path('vapt_assessment/', views.VaptAssessmentListView.as_view(), name='vapt_assessment'),
	path('config_review/', views.ConfigurationReviewListView.as_view(), name='config_review'),

	path('application_security/web_app/internal/', views.WebAppIntListView.as_view(), name='webappinternal'),
	path('application_security/web_app/external/', views.WebServIntListView.as_view(), name='webservinternal'),
	path('application_security/web_service/internal/', views.WebAppExtListView.as_view(), name='webappexternal'),
	path('application_security/web_service/external/', views.WebServExtListView.as_view(), name='webservexternal'),
	path('application_security/mobile_app/', views.MobAppListView.as_view(), name='mobapp'),

	path('application_security/<int:pk>/', views.ApplicationSecurityDetailView.as_view(), name='application_security_detail'),
	path('vapt_assessment/<int:pk>/', views.VaptAssessmentDetailView.as_view(), name='vapt_assessment_detail'),
	path('config_review/<int:pk>/', views.ConfigurationReviewDetailView.as_view(), name='config_review_detail'),

	path('request/application_security/', views.requestApplicationSecurity, name='request_application_security'),
	path('request/vapt_assessment/', views.requestVaptAssessment, name='request_vapt_assessment'),
	path('request/config_review/', views.requestConfigReview, name='request_config_review'),

	path('application_security/<int:pk>/update_status/', views.updateTaskApplication, name='update_status_application'),
	path('vapt_assessment/<int:pk>/update_status/', views.updateTaskVapt, name='update_status_vapt'),
	path('config_reveiw/<int:pk>/update_status/', views.updateTaskConfig, name='update_status_config'),
]
