from lib import views
from django.contrib import admin
from django.urls import path

app_name = 'lib'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
]
