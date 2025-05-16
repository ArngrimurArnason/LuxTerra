from django import forms
from django.core.exceptions import ValidationError
import re

COUNTRIES = [
    ('IS', 'Iceland'),
    ('US', 'United States'),
    # Add more as needed
]


class FinalizeStep1Form(forms.Form):
    street = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    country = forms.ChoiceField(choices=COUNTRIES, required=True)
    kennitala = forms.CharField(max_length=10, min_length=10, required=True)

    def clean_kennitala(self):
        value = self.cleaned_data['kennitala']
        if not value.isdigit():
            raise ValidationError("Kennitala must contain only digits.")
        if len(value) != 10:
            raise ValidationError("Kennitala must be exactly 10 digits.")
        return value

    def clean_street(self):
        value = self.cleaned_data.get('street', '').strip()

        # Reject special characters
        if re.search(r'[!"#]', value):
            raise ValidationError("Street address must not contain special characters like !\"#.")

        # Reject if only numbers
        if re.fullmatch(r'\d+', value):
            raise ValidationError("Street address cannot be just numbers.")

        parts = value.split()

        # Require at least one word and one number
        has_text = any(part.isalpha() for part in parts)
        has_number = any(part.isdigit() for part in parts)

        if not has_text or not has_number:
            raise ValidationError("Street must include both a name and a number (e.g., 'Main Street 12').")

        return value

    def clean_postal_code(self):
        value = self.cleaned_data['postal_code']
        if not value.isdigit():
            raise ValidationError("Postal code must contain only digits.")
        if len(value) != 3:
            raise ValidationError("Postal code must be exactly 3 digits.")
        return value

    def clean_city(self):
        value = self.cleaned_data['city'].strip()
        if not value.isalpha():
            raise ValidationError("City must contain only letters.")
        if len(value) <= 2:
            raise ValidationError("City name must be longer than 2 characters.")

        return value
