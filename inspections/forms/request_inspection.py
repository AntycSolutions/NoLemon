from django import forms

from inspections.models import Inspection

from ..models import InspectionRequest, Receipt


class RequestInspectionForm(forms.ModelForm):
    request_date = forms.DateTimeField(widget=forms.TextInput(attrs={
                                       'readonly': 'readonly'}))

    class Meta:
        model = InspectionRequest


class ReceiptForm(forms.ModelForm):
    INSPECTION_CHOICES = [(29.99, 'Option #1: $29.99 Expert Car Condition' +
                           ' Inspection Report and Video'),
                          (37.00, 'Option #2: $37.00 CAR PROOF REPORT'),
                          (56.00, 'Option #3: $56.00 Car Proof + Expert' +
                           ' Car Condition Inspection Report and Video' +
                           ' (Value Pack)')]

    # INSPECTIONS = [(i.pk, i) for i in Inspection.objects.all()]

    payment_level = forms.ChoiceField(widget=forms.RadioSelect,
                                      choices=INSPECTION_CHOICES)
    number = forms.CharField(max_length=64, widget=forms.HiddenInput)
    inspection = forms.ModelChoiceField(queryset=Inspection.objects.all(),
                                        widget=forms.HiddenInput)
    #                                choices=INSPECTIONS)

    class Meta:
        model = Receipt
