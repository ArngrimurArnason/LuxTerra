from django.forms import ModelForm
from property.models import Property
from django import forms
from django.forms.widgets import SelectDateWidget, SelectMultiple
from django.core.exceptions import ValidationError
import datetime



class ListPropertyForm(ModelForm):


    class Meta:
        model = Property
        exclude = ['property_id']
        fields = ['street', 'house_number', 'location', 'property_type', 'price','build_date', 'description', 'bathroom', 'bedrooms', 'size', 'thumbnail']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'build_date': forms.SelectDateWidget(
                years=range(1900, datetime.date.today().year + 1),
                empty_label=("day", "month", "year")),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'size': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_street(self):
        street = self.cleaned_data.get('street')
        if not street or len(street) < 2:
            raise ValidationError("Street name is too short.")
        return street

    def clean_house_number(self):
        number = self.cleaned_data.get('house_number')
        if number <= 0:
            raise ValidationError("House number must be positive.")
        return number

    def clean_location(self):
        loc = self.cleaned_data.get('location')
        if not loc:
            raise ValidationError("Location is required.")
        return loc

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc.strip()) < 20:
            raise ValidationError("Description must be at least 20 characters.")
        return desc

    def clean_bathroom(self):
        val = self.cleaned_data.get('bathroom')
        if val < 0:
            raise ValidationError("Number of bathrooms cannot be negative.")
        return val

    def clean_bedrooms(self):
        val = self.cleaned_data.get('bedrooms')
        if val < 0:
            raise ValidationError("Number of bedrooms cannot be negative.")
        return val

    def clean_size(self):
        size = self.cleaned_data.get('size')
        if size <= 0:
            raise ValidationError("Size must be greater than zero.")
        return size

