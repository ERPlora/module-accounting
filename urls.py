from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('journal/', views.journal_entries_list, name='journal'),
    path('reports/', views.dashboard, name='reports'),


    # Account
    path('accounts/', views.accounts_list, name='accounts_list'),
    path('accounts/add/', views.account_add, name='account_add'),
    path('accounts/<uuid:pk>/edit/', views.account_edit, name='account_edit'),
    path('accounts/<uuid:pk>/delete/', views.account_delete, name='account_delete'),
    path('accounts/<uuid:pk>/toggle/', views.account_toggle_status, name='account_toggle_status'),
    path('accounts/bulk/', views.accounts_bulk_action, name='accounts_bulk_action'),

    # JournalEntry
    path('journal_entries/', views.journal_entries_list, name='journal_entries_list'),
    path('journal_entries/add/', views.journal_entry_add, name='journal_entry_add'),
    path('journal_entries/<uuid:pk>/edit/', views.journal_entry_edit, name='journal_entry_edit'),
    path('journal_entries/<uuid:pk>/delete/', views.journal_entry_delete, name='journal_entry_delete'),
    path('journal_entries/bulk/', views.journal_entries_bulk_action, name='journal_entries_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
