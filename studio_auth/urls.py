from django.contrib import admin
from django.urls import path, include
from studio_auth import views

urlpatterns = [
    path('login/', views.login_on_website, name='studio_auth.login'),
    path('signup/', views.signup, name='studio_auth.signup'),
    path('signout/', views.signout, name='studio_auth.signout'),
]
