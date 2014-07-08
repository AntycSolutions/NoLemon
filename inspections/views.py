from django.contrib import messages
from django.shortcuts import render, redirect
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
    slug_field = "vin"
    slug_url_kwarg = "vin"

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.INFO,
                "We're sorry, we don't seem to have any inspections for the vehicle you're looking for.")
            return redirect('/vehicles', self.context)
        return self.render_to_response(self.context)
