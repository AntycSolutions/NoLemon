from django import forms

from ..models import InspectionRequest, Receipt


class RequestInspectionForm(forms.ModelForm):
    request_date = forms.DateTimeField(widget=forms.TextInput(attrs={
                                       'readonly': 'readonly'}))

    class Meta:
        model = InspectionRequest


class ReceiptForm(forms.ModelForm):
    INSPECTION_CHOICES = [(1, 'Option #1: $29.99 Expert Car Condition Inspection Report and Video'),
                          (2, 'Option #2: $37.00 CAR PROOF REPORT'),
                          (3, 'Option #3: $56.00 Car Proof + Expert Car Condition Inspection Report and Video (Value Pack)')]

    payment_level = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=INSPECTION_CHOICES)
    number = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Receipt
