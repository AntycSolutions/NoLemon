import datetime

from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from ..forms.request_inspection import RequestInspectionForm
from ..models import Vehicle, Seller, RequestInspection


class VehicleList(ListView):
    template_name = "testvehiclelist.html"
    model = Vehicle
    context_object_name = "vehicles"


class VehicleDetail(DetailView):
    template_name = "testvehicledetail.html"
    model = Vehicle
    slug_field = "vin"
    slug_url_kwarg = "vin"

    def get_context_data(self, **kwargs):
        context = super(VehicleDetail, self).get_context_data(**kwargs)
        form = None
        request_inspection = None
        try:
            seller = Seller.objects.get(email=self.request.user.email)
            requests = RequestInspection.objects.filter(seller=seller,
                                                        vehicle=self.object
                                                        )
            if requests.count() > 0:
                # This is for later if the form needs to be updated
                # form = RequestInspectionForm(instance=requests[0])
                # context['path'] = reverse_lazy("request_inspection_update",
                #                                kwargs={'vin': self.object.vin,
                #                                        'pk': requests[0].pk}
                #                                )
                request_inspection = requests[0]
            else:
                form = RequestInspectionForm(initial={
                    'seller': seller,
                    'vehicle': self.object,
                    'request_date': datetime.datetime.now()}
                )
                context['path'] = reverse_lazy("request_inspection_create",
                                               kwargs={'vin': self.object.vin}
                                               )
            form.fields['seller'].widget = forms.HiddenInput()
            form.fields['vehicle'].widget = forms.HiddenInput()
        except Exception as e:
            print("Exception:", e)
        context['form'] = form
        context['request_inspection'] = request_inspection
        return context

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any inspections "
                "for the vehicle you're looking for.")
            return redirect(reverse_lazy('vehicle_list'), self.context)
        return self.render_to_response(self.context)
