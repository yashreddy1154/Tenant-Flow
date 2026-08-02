from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .forms import OrganizationSignupForm, MemberEditForm
from django.contrib import messages
from apps.users.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = OrganizationSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = OrganizationSignupForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def invite_member_view(request):
    if request.user.role != 'Admin':
        messages.error(request, "You do not have permission to invite members.")
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role', 'Member')
        department = request.POST.get('department', '')
        if email:
            user, created = User.objects.get_or_create(email=email)
            if not created:
                if user.organization and user.organization != request.user.organization:
                    messages.error(request, f"User {email} already belongs to another organization.")
                    return redirect('team_management')
                elif user.organization == request.user.organization:
                    messages.info(request, f"User {email} is already in your team.")
                    return redirect('team_management')
            
            if created:
                # Create a user with unusable password if they are brand new
                user.set_unusable_password()
                
            user.organization = request.user.organization
            user.role = role
            user.department = department
            user.save()
            
            # Generate token and send email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            join_url = request.build_absolute_uri(reverse('join_organization', kwargs={'uidb64': uid, 'token': token}))
            
            send_mail(
                'You have been invited to TenantFlow',
                f'Click here to join your team: {join_url}',
                'noreply@tenantflow.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, f"Invite sent to {email}. Link: {join_url}")
            return redirect('home')
    return render(request, 'accounts/invite.html')

def join_organization_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                messages.success(request, "Your password has been set and you are now logged in.")
                return redirect('home')
        else:
            form = SetPasswordForm(user)
        return render(request, 'accounts/join.html', {'form': form})
    else:
        messages.error(request, "The invite link is invalid or has expired.")
        return redirect('login')
def verify_email_view(request):
    return render(request, 'accounts/verify_email.html')

def login_user(req):
    return render(req,"accounts/login_user.html")

def regester(req):
    return render(req,"accounts/register.html")

@login_required
def member_edit_view(request, pk):
    if request.user.role != 'Admin':
        messages.error(request, "Only Administrators can edit members.")
        return redirect('team_management')
        
    member = get_object_or_404(User, pk=pk, organization=request.user.organization)
    
    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {member.email}'s profile.")
            return redirect('team_management')
    else:
        form = MemberEditForm(instance=member)
        
    return render(request, 'organizations/member_edit.html', {'form': form, 'member': member})

@login_required
def member_remove_view(request, pk):
    if request.user.role != 'Admin':
        messages.error(request, "Only Administrators can remove members.")
        return redirect('team_management')
        
    member = get_object_or_404(User, pk=pk, organization=request.user.organization)
    
    if request.method == 'POST':
        member.organization = None
        member.role = 'Member'
        member.department = ''
        member.save()
        messages.success(request, f"Removed {member.email} from the organization.")
        return redirect('team_management')
        
    return render(request, 'organizations/member_remove_confirm.html', {'member': member})
