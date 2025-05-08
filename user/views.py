from django.shortcuts import render
# Create your views here.
def account_info(request):
    return render(request, 'account_info.html')

def offer_history(request):
    return render(request, 'offer_history.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def my_listings(request):
    return render(request, 'my_listings.html')

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'singup.html')


