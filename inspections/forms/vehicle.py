from django import forms

from inspections.models import Vehicle


class VehicleCreationForm(forms.ModelForm):

    class Meta:
        model = Vehicle
