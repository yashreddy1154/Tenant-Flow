from django.shortcuts import render

def project_list_view(request):
    return render(request, 'projects/project_list.html')

def project_create_view(request):
    return render(request, 'projects/project_create.html')

def project_detail_view(request):
    return render(request, 'projects/project_detail.html')
