from django import forms
from .models import Task
from apps.projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'status', 'priority', 'due_date', 'estimated_hours', 'assignee']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.organization:
            # Multi-tenant security: only show projects and users belonging to this organization
            self.fields['project'].queryset = Project.objects.filter(organization=user.organization)
            self.fields['assignee'].queryset = User.objects.filter(organization=user.organization)
