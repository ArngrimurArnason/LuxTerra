from django.urls import path
from . import views

urlpatterns = [
    path('', views.properties_view, name='properties'),
    path('list/', views.list_property, name='list_property'),
    path('property/<int:property_id>/', views.property_details, name='property_details'),
]