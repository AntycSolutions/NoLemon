from django import forms

from inspections.models import Vehicle


class VehicleCreationForm(forms.ModelForm):

    class Meta:
        model = Vehicle


class VehicleUpdateForm(forms.ModelForm):

    def clean_owner(self):
        return self.instance.owner

    class Meta:
        model = Vehicle
