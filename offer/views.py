from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from offer.forms.offer_forms import OfferForm
from offer.models import Offer
from property.models import Property
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

@login_required
def make_offer(request, property_id):

    property_obj = get_object_or_404(Property, pk=property_id)

    if str(property_obj.user.pk) == str(request.user.pk):
        messages.error(request, 'You are the seller and can not make an offer on your own listing')
        return redirect('property_details', property_id=property_id)

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.property = property_obj
            offer.offer_date = timezone.now()
            offer.save()
            return redirect('property_details', property_id=property_id)
    else:
        form = OfferForm()

    return render(request, 'offers/make_offer.html', {
        'form': form,
        'property': property_obj
    })

@login_required
def user_offers(request):
    offers = Offer.objects.filter(user=request.user)
    return render(request, 'offers/user_offers.html', {'offers': offers})

@login_required
def property_offers(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    if request.user != property_obj.user:
        return redirect('home')  # optional permission check

    offers = Offer.objects.filter(property=property_obj)
    return render(request, 'offers/property_offers.html', {'offers': offers, 'property': property_obj})

