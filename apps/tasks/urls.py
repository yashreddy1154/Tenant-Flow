from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list_view, name='task_list'),
    path('create/', views.task_create_view, name='task_create'),
    path('<int:pk>/', views.task_detail_view, name='task_detail'),
    path('<int:pk>/comment/', views.task_comment_create, name='task_comment_create'),
    path('<int:pk>/subtask/', views.task_subtask_create, name='task_subtask_create'),
    path('subtask/<int:pk>/toggle/', views.task_subtask_toggle, name='task_subtask_toggle'),
    path('labels/create/', views.task_label_create, name='task_label_create'),
    path('api/<int:pk>/status/', views.task_update_status_api, name='task_update_status_api'),
]
