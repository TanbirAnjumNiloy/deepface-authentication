from django.contrib import admin
from django.urls import path, include
from login import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',views.SignupPage,name='signup'),
    path('',views.LoginPage,name='login'),
    path('logout/',views.LogoutPage,name='logout'),
    path('passincorrect/',views.passincorrect,name='passincorrect'),
    
]

