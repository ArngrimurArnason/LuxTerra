from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.properties, name='properties'),  # All properties
    path('list_property/', views.list_property, name='list_property'), # List property
    path('<int:property_id>/property_details/', views.property_details, name='property_details'), # Property details for certain property
]