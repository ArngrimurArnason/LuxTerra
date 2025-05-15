from django import forms
from offer.models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_price']

    def clean_offer_price(self):
        price = self.cleaned_data.get('offer_price')
        if price is None or price <= 0:
            raise forms.ValidationError("Offer price must be greater than zero.")
        return price