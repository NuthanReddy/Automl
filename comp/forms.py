from django import forms

from comp.models import Submission


# class TeamForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ['lead', 'member']


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'language', 'algo']
