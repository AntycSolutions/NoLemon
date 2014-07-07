from django.shortcuts import render
from django.views.generic import ListView

from inspections.models import Vehicle


def home_page(request):
    return render(request, 'testindex.html')


class VehicleList(ListView):
    template_name = "testvehiclelist.html"
    model = Vehicle
    context_object_name = "vehicles"
