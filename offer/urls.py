from django.urls import path
from . import views

urlpatterns = [
    path('<int:property_id>/make/', views.make_offer, name='make_offer'),
]