


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms.list_property_forms import ListPropertyForm
from .models import Property, PropertyImages
from django.shortcuts import get_object_or_404
from django.db.models import Q


def properties_view(request):
  properties = Property.objects.filter(admin_approval=True)


  city = request.GET.get('city')
  min_price = request.GET.get('min_price')
  max_price = request.GET.get('max_price')
  property_type = request.GET.get('property_type')
  bedrooms = request.GET.get('bedrooms')
  postal_code = request.GET.get('postal_code')
  street_name = request.GET.get('street_name')
  order_by = request.GET.get('order_by')

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

  if city:
    properties = properties.filter(city__icontains=city)

  if postal_code:
    properties = properties.filter(post_code=postal_code)

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
      Q(city__icontains=street_name)
    )


  all_images = PropertyImages.objects.all()

  price_steps = [0, 50000000, 100000000, 150000000, 200000000, 250000000,
                 300000000, 350000000, 400000000]
  return render(request, 'all_properties.html', {
    "properties": properties,
    "property_images": all_images,
    "filters": {
      "city": city,
      "min_price": min_price,
      "max_price": max_price,
      "property_type": property_type,
      "bedrooms": bedrooms,
    },
    "prices": price_steps,
  })


@login_required(login_url='login')
def list_property(request):
    if request.method == "POST":
        form = ListPropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            messages.success(request, 'Property created.')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ListPropertyForm()

    return render(request, 'list_property.html', {
        'form': form
    })

def property_details(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    images = PropertyImages.objects.filter(property=property)
    return render(request, 'property_details.html', {
      "property": property,
      "images": images,
    })

