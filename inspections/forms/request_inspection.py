from django import forms

from ..models import InspectionRequest


class RequestInspectionForm(forms.ModelForm):
    request_date = forms.DateTimeField(widget=forms.TextInput(attrs={
                                       'readonly': 'readonly'}))

    class Meta:
        model = InspectionRequest
