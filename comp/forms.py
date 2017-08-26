from django import forms

from .models import Submission


class SubmitModel(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'team', 'comp', 'language', 'algo']
