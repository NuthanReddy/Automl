from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Dataset, Submission, UserProfile


class DatasetForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = ['type', 'name', 'file']


class UserProfileCreationForm(UserCreationForm):
    def __init__(self):
        super(UserProfileCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']


class UserProfileChangeForm(UserChangeForm):
    """
    Updating user profile info.
    """

    def __init__(self):
        super(UserProfileChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = UserProfile


class SubmitModel(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'team', 'comp', 'language', 'algo']
