from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account_info, name='account_info'),  # Account information page
    path('offer_history/', views.offer_history, name='offer_history'), # Account offer history
    path('edit_profile/', views.edit_profile, name='edit_profile'), # Edit profile
    path('my_listings/', views.my_listings, name='my_listings'), # Listings made by that user
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
]