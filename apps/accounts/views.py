from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return render(request, 'accounts/login.html')

def signup_view(request):
    return render(request, 'accounts/signup.html')

def verify_email_view(request):
    return render(request, 'accounts/verify_email.html')

def login_user(req):
    
    
    return render(req,"accounts/login_user.html")

def regester(req):
    
    
    return render(req,"accounts/register.html")
