from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import datetime

class FinalizeStep2Form(forms.Form):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mortgage', 'Mortgage'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.Select(attrs={'id': 'method-select'})
    )

    MONTH_CHOICES = [(f"{i:02}", f"{i:02}") for i in range(1, 13)]
    YEAR_CHOICES = [(str(i), f"20{i}") for i in range(25, 36)]

    # Credit card fields
    cardholder = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    cvc = forms.CharField(required=False)

    # Mortgage fields
    PROVIDER_CHOICES = [
        ("", "-- Select Bank --"),
        ("Arion Banki", "Arion Banki"),
        ("ÍslandsBanki", "ÍslandsBanki"),
        ("Landsbanki", "Landsbanki"),
        ("Kvika", "Kvika"),
    ]

    provider = forms.ChoiceField(
        choices=PROVIDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_cardholder(self):
        name = self.cleaned_data.get('cardholder', '').strip()
        if name and not all(part.isalpha() for part in name.split()):
            raise ValidationError("Cardholder name must contain only letters.")
        return name

    def clean_card_number(self):
        number = self.cleaned_data.get('card_number', '')
        if number and not re.fullmatch(r'(\d{4}-){3}\d{4}', number):
            raise ValidationError("Card number must be in the format 1111-2222-3333-4444.")
        return number

    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc', '')
        if cvc and not re.fullmatch(r'\d{3}', cvc):
            raise ValidationError("CVC must be exactly 3 digits.")
        return cvc

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('payment_method')

        if method == 'credit_card':
            required_fields = ['cardholder', 'card_number', 'expiry_month', 'expiry_year', 'cvc']
            for field in required_fields:
                if not cleaned.get(field):
                    self.add_error(field, 'This field is required.')

            # Validate expiry date is in the future
            month = cleaned.get('expiry_month')
            year = cleaned.get('expiry_year')

            if month and year:
                try:
                    expiry = datetime(year=int("20" + year), month=int(month), day=1)
                    now = datetime.now().replace(day=1)
                    if expiry < now:
                        self.add_error('expiry_year', 'Card expiry must be in the future.')
                except ValueError:
                    self.add_error('expiry_year', 'Invalid expiry date.')


        elif method == 'bank_transfer':
            pass

        elif method == 'mortgage':
            if not cleaned.get('provider'):
                self.add_error('provider', 'Please select a mortgage provider.')

        return cleaned
