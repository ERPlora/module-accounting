from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('journal/', views.journal, name='journal'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
]
