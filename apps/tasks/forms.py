from django import forms
from .models import Task, TaskComment, Subtask, TaskLabel
from apps.projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'status', 'priority', 'due_date', 'estimated_hours', 'assignee', 'labels']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.organization:
            # Multi-tenant security: only show projects and users belonging to this organization
            if user.role == 'Admin':
                self.fields['project'].queryset = Project.objects.filter(organization=user.organization)
            else:
                self.fields['project'].queryset = Project.objects.filter(organization=user.organization, team_leader=user)
            self.fields['assignee'].queryset = User.objects.filter(organization=user.organization)
            self.fields['labels'].queryset = TaskLabel.objects.filter(organization=user.organization)

class TaskLabelForm(forms.ModelForm):
    class Meta:
        model = TaskLabel
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add a subtask...'}),
        }
