import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from inspections.forms.request_inspection import ReceiptForm
from inspections.utilities import process_stripe, send_email
from no_lemon import settings

from ..forms.request_inspection import RequestInspectionForm
from ..forms.vehicle import VehicleCreationForm, VehicleUpdateForm
from ..models import Vehicle, Seller, InspectionRequest


class VehicleList(ListView):
    template_name = "vehicle/vehiclelist.html"
    model = Vehicle
    context_object_name = "vehicles"


class VehicleDetail(DetailView):
    template_name = "vehicle/vehicledetail.html"
    model = Vehicle
    slug_field = "vin"
    slug_url_kwarg = "vin"

    def get_context_data(self, **kwargs):
        context = super(VehicleDetail, self).get_context_data(**kwargs)
        form = None
        request_inspection = None
        try:
            seller = Seller.objects.get(email=self.request.user.email)
            requests = InspectionRequest.objects.filter(seller=seller,
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
            form.fields['request_date'].widget = forms.HiddenInput()
        except Exception:  # as e:
            #print("Exception:", e)
            pass

        # receipt form
        receipt_form = ReceiptForm()

        context['form'] = form
        context['request_inspection'] = request_inspection
        context['receipt_form'] = receipt_form

        context['option1'] = settings.VIEW_INSPECTION_CHARGE_LVL_1
        context['option2'] = settings.VIEW_INSPECTION_CHARGE_LVL_2
        context['option3'] = settings.VIEW_INSPECTION_CHARGE_LVL_3

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


class VehicleCreationView(CreateView):

    model = Vehicle
    form_class = VehicleCreationForm
    template_name = 'vehicle/vehiclecreate.html'
    success_url = reverse_lazy('vehicle_list')

    def get(self, request, *args, **kwargs):
        self.object = None

        form_class = self.get_form_class()
        try:
            form = self.get_form(form_class)
        except Seller.DoesNotExist:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, only sellers can order inspection reports.")
            return redirect(reverse_lazy('home'))

        form.fields['owner'].widget = forms.HiddenInput()

        return self.render_to_response(self.get_context_data(form=form))

    def get_initial(self):
        try:
            owner = Seller.objects.get(email=self.request.user.email)
        except:
            raise

        initial = {'owner': owner}
        return initial

    def post(self, request, *args, **kwargs):
        self.object = None
        # TODO: Integrate payment level options
        cost = settings.INSPECTION_REQUEST

        process_stripe(request.POST['stripeToken'], cost)

        return super(VehicleCreationView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        vehicle = self.request.POST['vin']
        self.success_url += vehicle

        form.save()
        InspectionRequest.objects.get_or_create(
            vehicle=Vehicle.objects.get(vin=vehicle),
            seller=Seller.objects.get(email=self.request.user.email),
            request_date=datetime.datetime.now())
        send_email()
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully added a vehicle " +
            "and requested an inspection for "
            + form.instance.__str__() + ". " +
            "You will be contacted by a NoLemon administrator " +
            "within 1 business days to confirm your request.")
        return HttpResponseRedirect(self.success_url)


class UpdateVehicleView(UpdateView):
    template_name = 'update.html'
    model = Vehicle
    form_class = VehicleUpdateForm

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            return reverse('update_vehicle', kwargs={'pk': pk})

    def get(self, request, **kwargs):
        try:
            Seller.objects.get(email=self.request.user.email)
            return self._get()
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, only sellers can update vehicles.")
            return redirect(reverse_lazy('home'))

    def _get(self):
        self.object = self.get_object()
        if not self.object:
            return redirect('/')
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form.fields['owner'].widget.attrs['readonly'] = True

        context = self.get_context_data(form=form)
        context['model_type'] = 'Vehicle'
        context['form_type'] = 'multipart/form-data'

        return self.render_to_response(context)
