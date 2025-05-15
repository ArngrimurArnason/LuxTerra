from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from offer.forms.offer_forms import OfferForm
from offer.models import Offer
from property.models import Property
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.views.decorators.http import require_POST

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
            offer.offer_expiry_date = timezone.now() + timedelta(days=7)
            offer.save()
            return redirect('property_details', property_id=property_id)
    else:
        form = OfferForm()

    return render(request, 'property_details.html', {
        'form': form,
        'property': property_obj
    })
def finalize_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offers/finalize_offer.html', {'offer': offer})

def incoming_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'offers/incoming_offers.html', {'offer': offer})


def make_counter_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, property__user=request.user)

    if request.method == 'POST':
        try:
            counter_price = int(request.POST.get('counter_price', 0))
            if counter_price <= 0:
                raise ValueError("Invalid price")

            # Set the new counter offer and mark as contingent
            offer.offer_price = counter_price
            offer.status = 'contingent'
            offer.save()

            messages.success(request, "Counter offer sent.")
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid counter offer price.")

    return redirect('incoming_offers')

def respond_to_counter_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, user=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['accepted', 'rejected']:
            offer.status = new_status
            offer.save()
            messages.success(request, f"You have {new_status} the counter-offer.")
        else:
            messages.error(request, "Invalid response.")

    return redirect('offer_history')


@require_POST
def update_offer_status(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, property__user=request.user)
    new_status = request.POST.get('status')
    if new_status in ['accepted', 'rejected', 'contingent']:
        offer.status = new_status
        offer.save()
        messages.success(request, f"Offer marked as {new_status}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect('incoming_offers')
