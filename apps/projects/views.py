from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from django.contrib import messages

@login_required
def project_list_view(request):
    # Only fetch projects for the user's organization
    projects = Project.objects.filter(organization=request.user.organization)
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            # Enforce multi-tenancy: link to the user's organization
            project.organization = request.user.organization
            project.created_by = request.user
            project.save()
            messages.success(request, f"Project '{project.name}' created successfully.")
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})

@login_required
def project_detail_view(request, pk):
    # Security Check: Ensure the project belongs to the user's organization
    project = get_object_or_404(Project, pk=pk, organization=request.user.organization)
    return render(request, 'projects/project_detail.html', {'project': project})
