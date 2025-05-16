from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms.list_property_forms import ListPropertyForm
from .models import LOCATION_CHOICES, Property, PropertyImages
from offer.models import Offer
from datetime import timedelta
from django.utils import timezone
from offer.forms.offer_forms import OfferForm

def group_postal_codes():
    '''Groups Icelandic postal codes by city from LOCATION_CHOICES.'''
    grouped = defaultdict(list)
    for full_value, _ in LOCATION_CHOICES:
        if " - " in full_value:
            code, city = full_value.split(" - ", 1)
            grouped[city].append(code)
    return dict(grouped)

def properties_view(request):
    '''Displays a list of approved properties with optional filters and sorting'''
    properties = Property.objects.filter(admin_approval=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    property_type = request.GET.get('property_type')
    bedrooms = request.GET.get('bedrooms')
    postal_code = request.GET.get('postal_code')
    street_name = request.GET.get('street_name')
    order_by = request.GET.get('order_by')

    # Sorting
    if order_by == 'price_asc':
        properties = properties.order_by('price')
    elif order_by == 'price_desc':
        properties = properties.order_by('-price')
    elif order_by == 'size_asc':
        properties = properties.order_by('size')
    elif order_by == 'size_desc':
        properties = properties.order_by('-size')
    elif order_by == 'date_asc':
        properties = properties.order_by('build_date')
    elif order_by == 'date_desc':
        properties = properties.order_by('-build_date')
    elif order_by == 'name_asc':
        properties = properties.order_by('street')
    elif order_by == 'name_desc':
        properties = properties.order_by('-street')

    # Filters
    if postal_code:
        properties = properties.filter(location__startswith=postal_code)

    if property_type:
        properties = properties.filter(property_type__iexact=property_type)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    if street_name:
        properties = properties.filter(
            Q(street__icontains=street_name) |
            Q(location__icontains=street_name) |
            Q(street__icontains=street_name.split(' ')[0], house_number__iexact=street_name.split(' ')[-1])
        )

    # Related images
    all_images = PropertyImages.objects.all()
    grouped_postal_codes = group_postal_codes()

    # Price filter options
    price_steps = [
        0, 50000000, 100000000, 150000000,
        200000000, 250000000, 300000000, 350000000, 400000000
    ]

    return render(request, 'properties/all_properties.html', {
        "properties": properties,
        "property_images": all_images,
        "filters": {
            "min_price": min_price,
            "max_price": max_price,
            "property_type": property_type,
            "bedrooms": bedrooms,
            "postal_code": postal_code,
            "street_name": street_name,
        },
        "prices": price_steps,
        "grouped_postal_codes": grouped_postal_codes,
    })




@login_required(login_url='login')
def list_property(request):
    '''Allows logged-in users to list a new property for sale'''

    if request.method == "POST":
        form = ListPropertyForm(request.POST, request.FILES)
        image_files = request.FILES.getlist('images')

        no_images_uploaded = not image_files
        thumbnail_missing = not request.FILES.get('thumbnail')

        if form.is_valid() and not no_images_uploaded:
            property_instance = form.save(commit=False)
            property_instance.user = request.user
            property_instance.save()

            for image in image_files:
                PropertyImages.objects.create(property=property_instance, image=image)

            messages.success(request, 'Listing published to properties. You can view it under your profile.')
            return redirect('list_property')

        if no_images_uploaded:
            messages.error(request, 'Please upload at least one photo.')
        if not form.is_valid():
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = ListPropertyForm()

    return render(request, 'properties/list_property.html', {'form': form})


def property_details(request, property_id):
    '''Displays detailed information for a single property'''
    prop = get_object_or_404(Property, pk=property_id)
    images = prop.images.all()

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            offer.property = prop
            offer.offer_date = timezone.now()
            offer.offer_expiry_date = timezone.now() + timedelta(days=30)
            offer.save()
            messages.success(request, "Your offer has been submitted successfully.")
            return redirect('property_details', property_id=prop.pk)
        else:
            messages.error(request, "There was a problem with your offer. Please fix the errors.")
    else:
        default_expiry = timezone.now().date() + timedelta(days=30)
        form = OfferForm(initial={'offer_expiry_date': default_expiry})

    return render(request, 'properties/property_details.html', {
        'property': prop,
        'images': images,
        'form': form,
    })
