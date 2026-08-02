from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Subtask, TaskComment, TaskLabel
from apps.projects.models import Project
from .forms import TaskForm, TaskStatusForm, TaskCommentForm, SubtaskForm, TaskLabelForm
from django.contrib import messages
from apps.notifications.models import Notification
from django.urls import reverse
from django.http import JsonResponse
import json
from apps.users.models import User

@login_required
def task_list_view(request):
    # Fetch tasks belonging to projects in the user's organization
    tasks = Task.objects.filter(project__organization=request.user.organization)
    
    query = request.GET.get('q', '')
    priority = request.GET.get('priority', 'All')
    assignee_id = request.GET.get('assignee', 'All')
    sort_by = request.GET.get('sort', '-created_at')

    if query:
        tasks = tasks.filter(title__icontains=query)
    
    if priority and priority != 'All':
        tasks = tasks.filter(priority=priority)
        
    if assignee_id and assignee_id != 'All':
        tasks = tasks.filter(assignee_id=assignee_id)
        
    tasks = tasks.order_by(sort_by)
    
    # Group tasks by status for a Kanban-style view
    todo_tasks = tasks.filter(status='Todo')
    in_progress_tasks = tasks.filter(status='In Progress')
    review_tasks = tasks.filter(status='Review')
    done_tasks = tasks.filter(status='Done')
    
    is_admin = request.user.role == 'Admin'
    is_leader = Project.objects.filter(organization=request.user.organization, team_leader=request.user).exists()
    
    assignees = User.objects.filter(organization=request.user.organization).order_by('email')
    
    context = {
        'tasks': tasks,
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'done_tasks': done_tasks,
        'total_tasks': tasks.count(),
        'can_create_task': is_admin or is_leader,
        'current_q': query,
        'current_priority': priority,
        'current_assignee': assignee_id,
        'current_sort': sort_by,
        'assignees': assignees
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create_view(request):
    is_admin = request.user.role == 'Admin'
    is_leader = Project.objects.filter(organization=request.user.organization, team_leader=request.user).exists()
    
    if not (is_admin or is_leader):
        messages.error(request, "You do not have permission to create tasks.")
        return redirect('task_list')
    if request.method == 'POST':
        # Pass the user to the form so it can filter the dropdowns
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            if task.assignee and task.assignee != request.user:
                Notification.objects.create(
                    recipient=task.assignee,
                    message=f"You have been assigned to a new task: {task.title}",
                    link=reverse('task_detail', args=[task.pk])
                )
            messages.success(request, f"Task '{task.title}' created successfully.")
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_create.html', {'form': form})

@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk, project__organization=request.user.organization)
    
    is_admin = request.user.role == 'Admin'
    is_leader = task.project.team_leader == request.user
    is_assignee = task.assignee == request.user
    
    if request.method == 'POST':
        if is_admin or is_leader:
            form = TaskForm(request.POST, instance=task, user=request.user)
        elif is_assignee:
            form = TaskStatusForm(request.POST, instance=task)
        else:
            messages.error(request, "You don't have permission to edit this task.")
            return redirect('task_detail', pk=task.pk)
            
        if form.is_valid():
            original_assignee = task.assignee
            form.save()
            
            # If assignee changed to someone else
            if task.assignee and task.assignee != original_assignee and task.assignee != request.user:
                Notification.objects.create(
                    recipient=task.assignee,
                    message=f"You have been assigned to the task: {task.title}",
                    link=reverse('task_detail', args=[task.pk])
                )
                
            messages.success(request, "Task updated successfully.")
            return redirect('task_detail', pk=task.pk)
    else:
        if is_admin or is_leader:
            form = TaskForm(instance=task, user=request.user)
        elif is_assignee:
            form = TaskStatusForm(instance=task)
        else:
            form = None

    context = {
        'task': task,
        'form': form,
        'can_edit_all': is_admin or is_leader,
        'can_edit_status': is_assignee,
        'comment_form': TaskCommentForm(),
        'subtask_form': SubtaskForm(),
    }
    return render(request, 'tasks/task_detail.html', context)

@login_required
def task_comment_create(request, pk):
    task = get_object_or_404(Task, pk=pk, project__organization=request.user.organization)
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            
            # Notify task assignee if they didn't write the comment
            if task.assignee and task.assignee != request.user:
                Notification.objects.create(
                    recipient=task.assignee,
                    message=f"{request.user.email} commented on your task: {task.title}",
                    link=reverse('task_detail', args=[task.pk])
                )
                
            messages.success(request, "Comment added.")
    return redirect('task_detail', pk=task.pk)

@login_required
def task_subtask_create(request, pk):
    task = get_object_or_404(Task, pk=pk, project__organization=request.user.organization)
    
    is_admin = request.user.role == 'Admin'
    is_leader = task.project.team_leader == request.user
    is_assignee = task.assignee == request.user
    
    if not (is_admin or is_leader or is_assignee):
        messages.error(request, "You don't have permission to add subtasks.")
        return redirect('task_detail', pk=task.pk)

    if request.method == 'POST':
        form = SubtaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            messages.success(request, "Subtask added.")
    return redirect('task_detail', pk=task.pk)

@login_required
def task_subtask_toggle(request, pk):
    subtask = get_object_or_404(Subtask, pk=pk, task__project__organization=request.user.organization)
    
    is_admin = request.user.role == 'Admin'
    is_leader = subtask.task.project.team_leader == request.user
    is_assignee = subtask.task.assignee == request.user
    
    if not (is_admin or is_leader or is_assignee):
        messages.error(request, "You don't have permission to modify subtasks.")
        return redirect('task_detail', pk=subtask.task.pk)

    if request.method == 'POST':
        subtask.is_completed = not subtask.is_completed
        subtask.save()
        
    return redirect('task_detail', pk=subtask.task.pk)

@login_required
def task_label_create(request):
    is_admin = request.user.role == 'Admin'
    is_leader = Project.objects.filter(organization=request.user.organization, team_leader=request.user).exists()
    
    if not (is_admin or is_leader):
        messages.error(request, "You do not have permission to create labels.")
        return redirect('task_list')

    if request.method == 'POST':
        form = TaskLabelForm(request.POST)
        if form.is_valid():
            label = form.save(commit=False)
            label.organization = request.user.organization
            label.save()
            messages.success(request, f"Label '{label.name}' created.")
            return redirect('task_list')
    else:
        form = TaskLabelForm()
    
    return render(request, 'tasks/task_label_create.html', {'form': form})

@login_required
def task_update_status_api(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, project__organization=request.user.organization)
        is_admin = request.user.role == 'Admin'
        is_leader = task.project.team_leader == request.user
        is_assignee = task.assignee == request.user
        
        if not (is_admin or is_leader or is_assignee):
            return JsonResponse({'error': 'Permission denied'}, status=403)
            
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            if new_status in dict(Task.STATUS_CHOICES):
                task.status = new_status
                task.save()
                return JsonResponse({'success': True, 'status': new_status})
            return JsonResponse({'error': 'Invalid status'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
