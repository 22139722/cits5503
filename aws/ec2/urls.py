from ec2 import views
from django.contrib import admin
from django.urls import path

app_name = 'ec2'

urlpatterns = [

    path('instances/all/', views.instances_list, name='instances_list'),
    path('instances/all/<str:json>', views.instances_list, name='instances_list'),

    path('instances/terminate/', views.terminate_instances, name='terminate_instances'),

    path('instances/old/', views.old_instances_list, name='old_instances_list'),
    path('instances/old/<str:json>', views.old_instances_list, name='old_instances_list'),

    path('instances/young/', views.young_instances_list, name='young_instances_list'),
    path('instances/young/<str:json>', views.young_instances_list, name='young_instances_list'),

]
