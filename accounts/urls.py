from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import *

urlpatterns = [
    path('home/', views.home, name='home'),
    path('teacher/', views.thome, name='thome'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('tsignup/', views.tsignup, name='tsignup'),
    path('tlogin/', views.tlogin, name='tlogin'),
    path('logout/', views.logout, name='logout'),
    path('tlogout/', views.tlogout, name='tlogout'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:account_id>/', views.dashboard, name='dashboard'),
    path('tdashboard/<int:teacher_id>/', views.tdashboard, name='tdashboard'),
    #path('index/', views.index, name = 'index')
    path('forms/', include('forms.urls'))
]