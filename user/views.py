from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User

from user.Forms.sign_up_form import SignUpForm


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


        try:
            user_obj = User.objects.get(email=email)

            # now try to authenticate
            user = authenticate(request, username=user_obj.username, password=password)


        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, 'Account created.')
            return redirect('login')
        else:

            messages.error(request, 'Please fix errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {
        'form': form})


def get_profile_image(request, user_id):
    profile = get_object_or_404(User, user__id=user_id)
    return JsonResponse({
        'profile_image_url': profile.profile_image.url if profile.profile_image else None
    })
