from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User

@login_required
def home_view(request):
    org = request.user.organization
    
    # Base queries for the organization
    org_projects = Project.objects.filter(organization=org)
    org_tasks = Task.objects.filter(project__organization=org)
    
    context = {
        'projects_count': org_projects.count(),
        'tasks_count': org_tasks.count(),
        'members_count': User.objects.filter(organization=org).count(),
        'recent_projects': org_projects.order_by('-created_at')[:3],
        'my_tasks': org_tasks.filter(assignee=request.user).exclude(status='Done').order_by('due_date')[:5]
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')
