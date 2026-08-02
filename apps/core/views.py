from django.shortcuts import render
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User

def home_view(request):
    context = {
        'projects_count': Project.objects.count(),
        'tasks_count': Task.objects.count(),
        'members_count': User.objects.count(),
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')
