from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('account/<int:user_id>/', views.account_info, name='account_info'),  # Account information page
    path('offer_history/', views.offer_history, name='offer_history'), # Account offer history
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('incoming_offers/', views.incoming_offers, name='incoming_offers'),
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('profile-image/<int:user_id>/', views.get_profile_image, name='get_profile_image'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout')
]