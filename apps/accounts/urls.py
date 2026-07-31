from django.urls import path
from . import views
urlpatterns = [
    path("login_user/",views.login_user,name="login_user"),
    path("regester/",views.regester,name="reg"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/', views.verify_email_view, name='verify_email'),

]
