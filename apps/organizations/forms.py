from django import forms
from .models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'industry_type', 'company_size', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Acme Corp'}),
            'description': forms.Textarea(attrs={'placeholder': 'Brief description of your company', 'rows': 3}),
            'industry_type': forms.TextInput(attrs={'placeholder': 'e.g. Software, Healthcare'}),
            'company_size': forms.NumberInput(attrs={'placeholder': 'Number of employees'}),
            'logo': forms.FileInput(attrs={'accept': 'image/*'})
        }
