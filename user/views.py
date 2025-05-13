from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
def account_info(request):
    return render(request, 'account_info.html')

def offer_history(request):
    return render(request, 'offer_history.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def my_listings(request):
    return render(request, 'my_listings.html')



User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("EMAIL:", email)
        print("PASSWORD:", password)

        try:
            user_obj = User.objects.get(email=email)
            print("Found user:", user_obj)

            # now try to authenticate
            user = authenticate(request, username=user_obj.username, password=password)
            print("Authenticated user:", user)

        except User.DoesNotExist:
            print("No user with that email.")
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')


