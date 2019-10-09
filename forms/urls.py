from django.urls import path
from . import views

urlpatterns = [
    path('regform/<int:account_id>/', views.regform, name='regform'),
    path('detail/<int:form_id>/', views.detail, name='detail'),
    #path('formlists/', views.formlists, name='formlists'),
    path('formlists/<str:ys_id>/', views.formlists, name='formlists'),
    path('plot/<str:ys_id>/', views.plot, name='plot')
]