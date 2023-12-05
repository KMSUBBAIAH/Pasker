# forms.py
from django import forms
from .models import ProtectedData

class PasswordLockerForm(forms.ModelForm):
    class Meta:
        model = ProtectedData
        fields = ['service_name', 'service_username', 'service_password']

class PasswordLockerUpdateForm(forms.ModelForm):
    class Meta:
        model = ProtectedData
        fields = ['service_name', 'service_username', 'service_password']
