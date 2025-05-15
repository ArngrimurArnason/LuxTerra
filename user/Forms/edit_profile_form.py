from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from user.models import User
import re


class EditProfileForm(ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Confirm New Password"
    )

    class Meta:
        model = User
        exclude = ['id']
        fields = ['username', 'email', 'national_id', 'address', 'logo', 'profile_img', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'national_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_national_id(self):
        nid = self.cleaned_data.get('national_id')
        if not str(nid).isdigit():
            raise ValidationError("SSN must contain only digits.")
        if len(str(nid)) != 10:
            raise ValidationError("SSN must be exactly 10 digits.")
        return nid

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise ValidationError("Username must not contain spaces.")
        if not username.isalpha():
            raise ValidationError("Username must contain only letters (a–z). No digits or symbols.")
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Email already in use.")
        return email

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address and len(address) > 30:
            raise ValidationError("Address too long.")
        return address

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password')
        pw2 = cleaned_data.get('confirm_password')

        if pw1 or pw2:
            if pw1 != pw2:
                raise ValidationError("New passwords do not match.")

