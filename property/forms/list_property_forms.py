from django.forms import ModelForm
from property.models import Property
from django import forms
from django.forms.widgets import SelectDateWidget, SelectMultiple
import datetime





class ListPropertyForm(ModelForm):

    class Meta:
        model = Property
        exclude = ['property_id']
        fields = ['street', 'house_number', 'location', 'property_type', 'price', 'description', 'bathroom', 'bedrooms', 'size', 'property_status', 'thumbnail']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'build_date': SelectDateWidget(
                years=range(1900, datetime.date.today().year + 1),
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'size': forms.NumberInput(attrs={'class': 'form-control quantity-input', 'min': 0}),
            'property_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


