from django import forms

from bootstrap3_datetime.widgets import DateTimePicker

from inspections.models import Inspection


class InspectionUpdateForm(forms.ModelForm):

    date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=DateTimePicker(options={"format": "YYYY-MM-DD hh:mm a"}))

    def clean_vehicle(self):
        return self.instance.vehicle

    def clean_mechanic(self):
        return self.instance.mechanic

    def clean_views(self):
        return self.instance.views

    class Meta:
        model = Inspection


class InspectionCreateForm(forms.ModelForm):

    class Meta:
        model = Inspection
