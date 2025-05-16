from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from .Forms.edit_profile_form import EditProfileForm
from .models import User
from property.models import Property
from django.contrib.auth.decorators import login_required
from user.Forms.sign_up_form import SignUpForm
from offer.models import Offer
from django.utils import timezone


# Create your views here.
def account_info(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    properties = Property.objects.filter(user_id=user.user_id)

    return render(request, 'account_info.html', {
        'user': user,
        'properties': properties
    })

def offer_history(request):
    Offer.objects.filter(user=request.user, offer_expiry_date__lt=timezone.now()).delete()
    user_offers = Offer.objects.select_related('property', 'user').filter(
        user=request.user,
        property__isnull=False,
        property__user__isnull=False
    )
    return render(request, 'offers/offer_history.html', {'offers': user_offers})



def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
            user.save()
            messages.success(request, "Profile updated.")
            return redirect('account_info',  user_id=user.user_id)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})

def incoming_offers(request):
    offers = Offer.objects.select_related('property', 'user').filter(property__user=request.user)
    return render(request, 'offers/incoming_offers.html', {'offers': offers})


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
