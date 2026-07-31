from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login_user(req):
    
    
    return render(req,"accounts/login_user.html")

def regester(req):
    
    
    return render(req,"accounts/register.html")
