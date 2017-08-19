from django import forms
from django.contrib.auth.models import User
from .models import Dataset


class DatasetForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['type', 'name', 'file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

