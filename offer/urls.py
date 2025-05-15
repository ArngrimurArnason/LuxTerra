from django.urls import path
from . import views

urlpatterns = [
    path('<int:property_id>/make/', views.make_offer, name='make_offer'),
    path('finalize/<int:offer_id>/', views.finalize_offer, name='finalize_offer'),
    path('offers/<int:offer_id>/update/', views.update_offer_status, name='update_offer_status'),
    path('offers/<int:offer_id>/counter/', views.make_counter_offer, name='make_counter_offer'),
    path('offers/<int:offer_id>/respond/', views.respond_to_counter_offer, name='respond_to_counter_offer'),
]