from django import forms

from .models import Submission


class SubmissionForm(forms.ModelForm):
    name = forms.CharField(required=False)
    code = forms.FileField(required=True)

    class Meta:
        model = Submission
        fields = ('name', 'code',)
