from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Submission


class UserProfileCreationForm(UserCreationForm):
    def __init__(self):
        super(UserProfileCreationForm, self).__init__(*args, **kargs)
        del self.fields['email']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'location', 'country']


class UserProfileChangeForm(UserChangeForm):
    """
    Updating user profile info.
    """

    def __init__(self):
        super(UserProfileChangeForm, self).__init__(*args, **kargs)
        del self.fields['email']

    class Meta:
        model = User


class SubmitModel(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'team', 'comp', 'language', 'algo']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    template_name = '/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )
