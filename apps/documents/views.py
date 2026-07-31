from django.shortcuts import render

def document_list_view(request):
    return render(request, 'documents/document_list.html')
