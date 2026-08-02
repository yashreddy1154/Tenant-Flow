from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrganizationForm
from django.contrib import messages
from apps.users.models import User

@login_required
def create_org_view(request):
    return render(request, 'organizations/create_org.html')

@login_required
def org_settings_view(request):
    if request.user.role != 'Admin':
        messages.error(request, "You do not have permission to access Organization Settings.")
        return redirect('home')

    org = request.user.organization
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, "Organization details updated successfully.")
            return redirect('org_settings')
    else:
        form = OrganizationForm(instance=org)
    
    return render(request, 'organizations/org_settings.html', {'form': form, 'org': org})

@login_required
def team_management_view(request):
    org = request.user.organization
    members = User.objects.filter(organization=org).order_by('date_joined')
    return render(request, 'organizations/team_management.html', {'members': members, 'org': org})

@login_required
def billing_view(request):
    if request.user.role != 'Admin':
        messages.error(request, "Only Administrators can access billing.")
        return redirect('home')
        
    context = {
        'plan_name': 'Pro Plan',
        'price': '₹999/month',
        'next_billing_date': 'Oct 1, 2026',
        'users_used': User.objects.filter(organization=request.user.organization).count(),
        'users_limit': 50,
        'storage_used': '2.4 GB',
        'storage_limit': '10 GB'
    }
    return render(request, 'organizations/billing.html', context)

@login_required
def roles_permissions_view(request):
    if request.user.role != 'Admin':
        messages.error(request, "Only Administrators can access roles and permissions.")
        return redirect('home')
        
    # Static data representing our system's RBAC
    roles = [
        {
            'name': 'Admin',
            'description': 'Full access to all organization settings, billing, and all projects.',
            'users_count': User.objects.filter(organization=request.user.organization, role='Admin').count(),
            'permissions': ['Manage Organization Settings', 'Manage Billing', 'Invite/Remove Members', 'Create Projects', 'Edit All Projects', 'Delete Documents']
        },
        {
            'name': 'Manager',
            'description': 'Can manage projects they lead and tasks assigned to them.',
            'users_count': User.objects.filter(organization=request.user.organization, role='Manager').count(),
            'permissions': ['View Projects', 'Edit Led Projects', 'Create Tasks (Led Projects)', 'Upload Documents']
        },
        {
            'name': 'Member',
            'description': 'Basic access to assigned tasks and public documents.',
            'users_count': User.objects.filter(organization=request.user.organization, role='Member').count(),
            'permissions': ['View Projects', 'Update Assigned Tasks Status', 'Comment on Tasks', 'Upload Documents']
        }
    ]
    
    return render(request, 'organizations/roles.html', {'roles': roles})
