from django import forms

from ..models import Inspection


class VideoForm(forms.ModelForm):

    class Meta:
        model = Inspection
