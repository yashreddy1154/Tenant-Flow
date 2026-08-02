from django.urls import path
from . import views
urlpatterns = [
    path("login_user/",views.login_user,name="login_user"),
    path("regester/",views.regester,name="reg"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('invite/', views.invite_member_view, name='invite_member'),
    path('join/<uidb64>/<token>/', views.join_organization_view, name='join_organization'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
]
