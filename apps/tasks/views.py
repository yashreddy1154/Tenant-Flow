from django.shortcuts import render

def task_list_view(request):
    return render(request, 'tasks/task_list.html')

def task_create_view(request):
    return render(request, 'tasks/task_create.html')

def task_detail_view(request):
    return render(request, 'tasks/task_detail.html')
