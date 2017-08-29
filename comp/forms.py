from django import forms

from .models import Submission


# class TeamForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ['lead', 'member']


class SubmitModel(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'user', 'comp', 'language', 'algo']
