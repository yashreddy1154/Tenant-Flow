from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib import messages

@login_required
def task_list_view(request):
    # Fetch tasks belonging to projects in the user's organization
    tasks = Task.objects.filter(project__organization=request.user.organization)
    
    # Group tasks by status for a Kanban-style view
    todo_tasks = tasks.filter(status='Todo')
    in_progress_tasks = tasks.filter(status='In Progress')
    review_tasks = tasks.filter(status='Review')
    done_tasks = tasks.filter(status='Done')
    
    context = {
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'done_tasks': done_tasks,
        'total_tasks': tasks.count()
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create_view(request):
    if request.method == 'POST':
        # Pass the user to the form so it can filter the dropdowns
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"Task '{task.title}' created successfully.")
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
def task_detail_view(request, pk):
    # Security check: Ensure the task belongs to a project in the user's organization
    task = get_object_or_404(Task, pk=pk, project__organization=request.user.organization)
    return render(request, 'tasks/task_detail.html', {'task': task})
