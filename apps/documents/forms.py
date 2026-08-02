from django import forms
from .models import Document
from apps.projects.models import Project

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file', 'project']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Document Name', 'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.organization:
            if user.role == 'Admin':
                self.fields['project'].queryset = Project.objects.filter(organization=user.organization)
            else:
                self.fields['project'].queryset = Project.objects.filter(organization=user.organization, team_members=user)
