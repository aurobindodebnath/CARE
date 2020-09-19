from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from activities import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('loggedin/', views.loggedin, name='loggedin'),

    path('loggedin/appsec/', views.appsec, name='appsec'),
    path('loggedin/vapt/', views.vapt, name='vapt'),
    path('loggedin/config/', views.config, name='config'),
    path('loggedin/activities/', views.activities, name='activities'),

    path('loggedin/appsec/<int:unique_id>/', views.appsecDetail, name='appsec_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)