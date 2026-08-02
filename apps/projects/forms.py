from django import forms
from .models import Project
from apps.users.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date', 'end_date', 'budget', 'team_leader', 'team_members']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'team_members': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        if org:
            self.fields['team_leader'].queryset = User.objects.filter(organization=org)
            self.fields['team_leader'].label_from_instance = lambda obj: f"{obj.email} ({obj.role})"
            
            self.fields['team_members'].queryset = User.objects.filter(organization=org)
            self.fields['team_members'].label_from_instance = lambda obj: f"{obj.email} ({obj.role})"
