# forms.py
from django import forms
from offer.models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_price']

