from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Billing
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['meter_id', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        widgets = {
            'meter_id': forms.TextInput(attrs={'class': 'form-control', 'id': "inputPassword4"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': "inputPassword4"}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': "inputPassword4"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': "inputPassword4"}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': "inputPassword4"}),
        }


class CreateTariff(forms.Form):
    class Meta:
        model = Billing
        fields = '__all__'
