from django.shortcuts import render
from django.views.generic import ListView, DetailView

from inspections.models import Vehicle


def home_page(request):
    return render(request, 'testindex.html')


class VehicleList(ListView):
    template_name = "testvehiclelist.html"
    model = Vehicle
    context_object_name = "vehicles"


class VehicleDetail(DetailView):
    template_name = "testvehicledetail.html"
    model = Vehicle
    context_object_name = "vehicle"

    def get(self, request, *args, **kwargs):
        print("Ya got me!")
        return super(VehicleDetail, self).get(request, args, kwargs)
