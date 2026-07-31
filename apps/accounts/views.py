from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

def signup_view(request):
    return render(request, 'accounts/signup.html')

def verify_email_view(request):
    return render(request, 'accounts/verify_email.html')
