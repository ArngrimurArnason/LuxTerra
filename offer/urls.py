from django.urls import path
from . import views

urlpatterns = [
    path('review_offer/', views.review_offer, name='review_offer')
]