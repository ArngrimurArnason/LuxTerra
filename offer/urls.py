from django.urls import path
from . import views

urlpatterns = [
    path('<int:property_id>/make/', views.make_offer, name='make_offer'),
    path('offers/<int:offer_id>/update/', views.update_offer_status, name='update_offer_status'),
    path('offers/<int:offer_id>/counter/', views.make_counter_offer, name='make_counter_offer'),
    path('offers/<int:offer_id>/respond/', views.respond_to_counter_offer, name='respond_to_counter_offer'),
    path('<int:offer_id>/finalize/step1/', views.finalize_step1, name='finalize_step1'),
    path('<int:offer_id>/finalize/step2/', views.finalize_step2, name='finalize_step2'),
    path('<int:offer_id>/finalize/step3/', views.finalize_step3, name='finalize_step3'),
    path('<int:offer_id>/finalize/step4/', views.finalize_step4, name='finalize_step4'),
]