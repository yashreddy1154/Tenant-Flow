from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_org_view, name='create_org'),
    path('settings/', views.org_settings_view, name='org_settings'),
    path('team/', views.team_management_view, name='team_management'),
    path('billing/', views.billing_view, name='billing'),
]
