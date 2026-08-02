from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .forms import OrganizationSignupForm
from django.contrib import messages
from apps.users.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Create a user with unusable password
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()
                user.organization = request.user.organization
                user.role = 'Member'
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
            messages.success(request, f"Invite sent to {email}")
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
