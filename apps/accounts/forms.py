from django import forms
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization

User = get_user_model()

class OrganizationSignupForm(forms.ModelForm):
    organization_name = forms.CharField(max_length=100, required=True, label="Organization Name")
    industry_type = forms.CharField(max_length=100, required=False, label="Industry/Type")
    company_size = forms.IntegerField(required=False, label="Company Size")
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def save(self, commit=True):
        # 1. Create Organization
        org = Organization.objects.create(
            name=self.cleaned_data['organization_name'],
            industry_type=self.cleaned_data.get('industry_type', ''),
            company_size=self.cleaned_data.get('company_size', None)
        )
        
        # 2. Create User
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.organization = org
        user.role = 'Admin' # The creator is the admin
        
        if commit:
            user.save()
            
        return user

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'department']
        widgets = {
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Engineering, Sales'}),
        }
