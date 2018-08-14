from iam import views
from django.contrib import admin
from django.urls import path

app_name = 'iam'

urlpatterns = [
    path('users/list/all', views.users_list, name='users_list'),

    # JSON responses intended for AJAX
    path('users/list/active', views.active_users_list, name='active_users_list'),
    path('users/list/active/<str:json>', views.active_users_list, name='active_users_list'),
    path('users/list/inactive', views.inactive_users_list, name='inactive_users_list'),
    path('users/list/inactive/<str:json>', views.inactive_users_list, name='inactive_users_list'),
    path('users/list/delete', views.delete_inactive_users, name='delete_inactive_users'),
]
