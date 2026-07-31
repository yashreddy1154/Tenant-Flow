from django.shortcuts import render

def create_org_view(request):
    return render(request, 'organizations/create_org.html')

def org_settings_view(request):
    return render(request, 'organizations/org_settings.html')

def team_management_view(request):
    return render(request, 'organizations/team_management.html')

def billing_view(request):
    return render(request, 'organizations/billing.html')
