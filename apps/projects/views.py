from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from django.contrib import messages

@login_required
def project_list_view(request):
    projects = Project.objects.filter(organization=request.user.organization)
    
    query = request.GET.get('q', '')
    status = request.GET.get('status', 'Active')
    sort_by = request.GET.get('sort', '-created_at')

    if query:
        projects = projects.filter(name__icontains=query)
    
    if status and status != 'All':
        projects = projects.filter(status=status)
        
    projects = projects.order_by(sort_by)
    
    context = {
        'projects': projects,
        'current_q': query,
        'current_status': status,
        'current_sort': sort_by,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_create_view(request):
    if request.user.role != 'Admin':
        messages.error(request, "Only Administrators can create projects.")
        return redirect('project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, organization=request.user.organization)
        if form.is_valid():
            project = form.save(commit=False)
            # Enforce multi-tenancy: link to the user's organization
            project.organization = request.user.organization
            project.created_by = request.user
            project.save()
            messages.success(request, f"Project '{project.name}' created successfully.")
            return redirect('project_list')
    else:
        form = ProjectForm(organization=request.user.organization)
    return render(request, 'projects/project_create.html', {'form': form})

@login_required
def project_detail_view(request, pk):
    # Security Check: Ensure the project belongs to the user's organization
    project = get_object_or_404(Project, pk=pk, organization=request.user.organization)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_edit_view(request, pk):
    project = get_object_or_404(Project, pk=pk, organization=request.user.organization)
    
    # RBAC Check
    if request.user.role != 'Admin' and request.user != project.team_leader:
        messages.error(request, "You do not have permission to edit this project.")
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, organization=request.user.organization)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.name}' updated successfully.")
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project, organization=request.user.organization)
        
    return render(request, 'projects/project_create.html', {'form': form, 'is_edit': True, 'project': project})
