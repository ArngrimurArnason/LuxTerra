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
            messages.success(request, 'Your offer has been submitted, check the status under offer history ')
            return redirect('property_details', property_id=property_id)
    else:
        form = OfferForm()

    return render(request, 'property_details.html', {
        'form': form,
        'property': property_obj
    })

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
        status = request.POST.get('status')

        # If buyer is countering again
        if status == 'pending':
            try:
                counter_price = int(request.POST.get('counter_price'))
                if counter_price <= 0:
                    raise ValueError("Invalid offer")

                offer.offer_price = counter_price
                offer.status = 'pending'  # back to seller to decide
                offer.save()

                messages.success(request, "Your counter offer has been sent.")
            except (ValueError, TypeError):
                messages.error(request, "Please enter a valid price.")
        elif status in ['accepted', 'rejected']:
            offer.status = status
            offer.save()
            messages.success(request, f"You have {status} the counter offer.")
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


COUNTRIES = ["Iceland", "Norway", "Sweden", "Denmark", "Finland"]

@login_required
def finalize_step1(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, user=request.user)
    data = request.session.get('finalize_data', {})

    if request.method == 'POST':
        request.session['finalize_data'] = {
            'street': request.POST.get('street'),
            'city': request.POST.get('city'),
            'postal_code': request.POST.get('postal_code'),
            'country': request.POST.get('country'),
            'kennitala': request.POST.get('kennitala')
        }
        return redirect('finalize_step2', offer_id=offer_id)

    return render(request, 'offers/finalize_step1.html', {
        'offer': offer,
        'countries': COUNTRIES,
        'data': data,
        'step_number': 1
    })


@login_required
def finalize_step2(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, user=request.user)
    finalize_data = request.session.get('finalize_data', {})

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        finalize_data['payment_method'] = payment_method

        if payment_method == 'credit_card':
            finalize_data['cardholder'] = request.POST.get('cardholder')
            finalize_data['card_number'] = request.POST.get('card_number')
            finalize_data['expiry_date'] = request.POST.get('expiry_date')
            finalize_data['cvc'] = request.POST.get('cvc')
        elif payment_method == 'bank_transfer':
            finalize_data['iban'] = request.POST.get('iban')
            finalize_data['swift'] = request.POST.get('swift')
        elif payment_method == 'mortgage':
            finalize_data['provider'] = request.POST.get('provider')

        request.session['finalize_data'] = finalize_data
        return redirect('finalize_step3', offer_id=offer_id)

    return render(request, 'offers/finalize_step2.html', {
        'offer': offer,
        'data': finalize_data,
        'step_number': 2})


@login_required
def finalize_step3(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, user=request.user)
    data = request.session.get('finalize_data', {})

    if request.method == 'POST':
        return redirect('finalize_step4', offer_id=offer_id)

    return render(request, 'offers/finalize_step3.html', {'offer': offer, 'data': data, 'step_number': 3})


@login_required
def finalize_step4(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id, user=request.user)
    data = request.session.pop('finalize_data', {})

    property_obj = offer.property
    offer.delete()
    property_obj.delete()

    return render(request, 'offers/finalize_step4.html', {'data': data, 'step_number': 4})