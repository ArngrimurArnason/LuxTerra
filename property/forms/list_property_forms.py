from django.forms import ModelForm
from property.models import property
from django import forms


class ListPropertyForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Property
        exclude = ['id']
        fields = ['streetname', 'house_number', 'city', 'post_code', 'property_type', 'price', 'description', 'bathroom', 'bedrooms', 'bio', 'bio']
        widgets = {
            'streetname': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.Integerinput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'post_code': forms.Integerinput(attrs={'class': 'form-control'}),
            'property_type': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'build_date': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'bathroom': forms.Textarea(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password')
        pw2 = cleaned_data.get('confirm_password')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match.")
