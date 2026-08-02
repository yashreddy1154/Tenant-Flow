from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Document
from .forms import DocumentUploadForm

@login_required
def document_list_view(request):
    documents = Document.objects.filter(organization=request.user.organization)
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            document = form.save(commit=False)
            document.organization = request.user.organization
            document.uploaded_by = request.user
            document.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect('document_list')
    else:
        form = DocumentUploadForm(user=request.user)
    return render(request, 'documents/document_upload.html', {'form': form})

@login_required
def document_delete_view(request, pk):
    document = get_object_or_404(Document, pk=pk, organization=request.user.organization)
    
    if request.user.role != 'Admin' and document.uploaded_by != request.user:
        messages.error(request, "You do not have permission to delete this document.")
        return redirect('document_list')
        
    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document deleted.")
        return redirect('document_list')
        
    return render(request, 'documents/document_delete.html', {'document': document})
