from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from accounts.models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    location = forms.CharField(required=True)
    phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'location',
            'phone'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.location = self.cleaned_data['location']
            user_profile.phone = self.cleaned_data['phone']
            user_profile.save()

        return user


class EditProfileForm(UserChangeForm):
    template_name = '/something/else'

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )
