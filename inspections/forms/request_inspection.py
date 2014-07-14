from django import forms

from ..models import RequestInspection


class RequestInspectionForm(forms.ModelForm):
    request_date = forms.DateTimeField(widget=forms.TextInput(attrs={
                                       'readonly': 'readonly'}))

    class Meta:
        model = RequestInspection
