from django import forms

from inspections.models import Inspection


class InspectionUpdateForm(forms.ModelForm):

    def clean_vehicle(self):
        return self.instance.vehicle

    def clean_mechanic(self):
        return self.instance.mechanic

    def clean_views(self):
        return self.instance.views

    class Meta:
        model = Inspection
