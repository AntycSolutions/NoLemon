import datetime

from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms.rating import RatingForm
from .forms.request_inspection import RequestInspectionForm
from .models import Vehicle, Inspection, Seller, Customer, Rating, \
    RequestInspection, Mechanic


def home_page(request):
    return render(request, 'testindex.html')


class MechanicList(ListView):
    # fix me
    template_name = "testmechaniclist.html"
    model = Mechanic
    context_object_name = "mechanics"

    def get_context_data(self, **kwargs):
        context = super(MechanicList, self).get_context_data(**kwargs)
        context["static_map"] = ""
        context["intera_map"] = []
        for mechanic in self.get_queryset():
            full_address = mechanic.full_address().replace(" ", "+")
            context["static_map"] += full_address + "|"
            context["intera_map"] += [full_address]
        context["static_map"] = context["static_map"][:-1]
        return context


class MechanicDetail(DetailView):
    template_name = "testmechanicdetail.html"
    model = Mechanic
    slug_field = "email"
    slug_url_kwarg = "email"

    def get_context_data(self, **kwargs):
        context = super(MechanicDetail, self).get_context_data(**kwargs)
        full_address = self.object.full_address().replace(" ", "+")
        context["intera_map"] = full_address
        return context

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any mechanics "
                "you're looking for.")
            # fix me
            return redirect('/mechanics/', self.context)
        return self.render_to_response(self.context)


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
            return redirect('/vehicles/', self.context)
        return self.render_to_response(self.context)


class InspectionList(ListView):
    template_name = "testinspectionlist.html"
    model = Inspection
    context_object_name = "inspections"


class InspectionDetail(DetailView):
    template_name = "testinspectiondetail.html"
    model = Inspection
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any inspections "
                "you're looking for.")
            return redirect('/inspections/', self.context)
        return self.render_to_response(self.context)


class SellerList(ListView):
    template_name = "testsellerlist.html"
    model = Seller
    context_object_name = "sellers"


class SellerDetail(DetailView):
    template_name = "testsellerdetail.html"
    model = Seller
    slug_field = "email"
    slug_url_kwarg = "email"

    def get_context_data(self, **kwargs):
        context = super(SellerDetail, self).get_context_data(**kwargs)
        form = None
        try:
            customer = Customer.objects.get(email=self.request.user.email)
            ratings = Rating.objects.filter(seller=self.object,
                                            customer=customer
                                            )
            if ratings.count() > 0:
                form = RatingForm(instance=ratings[0])
                context['path'] = reverse_lazy("rating_update",
                                               kwargs={'pk': ratings[0].pk}
                                               )
            else:
                form = RatingForm(initial={'seller': self.object,
                                           'customer': customer}
                                  )
                context['path'] = reverse_lazy("rating_create")
            form.fields['seller'].widget = forms.HiddenInput()
            form.fields['customer'].widget = forms.HiddenInput()
        except Exception as e:
            print("Exception:", e)
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any sellers "
                "you're looking for.")
            return redirect('/sellers/', self.context)
        return self.render_to_response(self.context)


class RatingFormCreateView(CreateView):
    model = Rating
    fields = ['rating']
    success_url = '/sellers/'
    form_class = RatingForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += form.instance.seller.email
        return super(RatingFormCreateView, self).form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(
                    self.request, messages.ERROR,
                    form.fields[field].label
                    + ". " + error)
        return redirect('/sellers/' + form.instance.seller.email)


class RatingFormUpdateView(UpdateView):
    model = Rating
    fields = ['rating']
    success_url = '/sellers/'
    form_class = RatingForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += form.instance.seller.email
        return super(RatingFormUpdateView, self).form_valid(form)


# class RatingFormDeleteView(DeleteView):
#     model = Rating
# success_url = reverse_lazy(#fix me)


class RequestInspectionCreateView(CreateView):

    model = RequestInspection
    success_url = '/vehicles/'
    form_class = RequestInspectionForm
    template_name = 'testrequestinspection.html'

    def get_context_data(self, **kwargs):
        context = super(
            RequestInspectionCreateView, self).get_context_data(**kwargs)
        vehicle = kwargs['vehicle']
        form = None
        request_inspection = None
        try:
            seller = Seller.objects.get(email=self.request.user.email)
            requests = RequestInspection.objects.filter(seller=seller,
                                                        vehicle=vehicle
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
                    'vehicle': vehicle,
                    'request_date': datetime.datetime.now()}
                )
                context['path'] = reverse_lazy("request_inspection_create",
                                               kwargs={'vin': vehicle.vin}
                                               )
            form.fields['seller'].widget = forms.HiddenInput()
            form.fields['vehicle'].widget = forms.HiddenInput()
        except Exception as e:
            print("Exception:", e)
        context['form'] = form
        context['request_inspection'] = request_inspection
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        vin = None
        if 'vehicle' in request.GET:
            vin = request.GET['vehicle']
        else:
            vin = request.session.get('vehicle')
        vehicle = Vehicle.objects.get(vin=vin)
        print(vehicle)
        kwargs['vehicle'] = vehicle

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        kwargs['form'] = form

        return self.render_to_response(self.get_context_data(form=form,
                                                             vehicle=vehicle))

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully requested an inspection for "
            + form.instance.seller.email)
        self.success_url += form.instance.vehicle.vin
        return super(RequestInspectionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                error_msg = form.fields[field].label + ". "
                print("This error is: ", error_msg)
                error_msg += error
                print("This error is: ", error_msg)
                messages.add_message(
                    self.request, messages.ERROR,
                    form.fields[field].label
                    + ". " + error)
        return redirect('/vehicles/' + form.instance.vehicle.vin
                        + "/request/inspection/")


class RequestInspectionUpdateView(UpdateView):
    model = RequestInspection
    success_url = '/vehicles/'
    form_class = RequestInspectionForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully updated a request for an inspection for "
            + form.instance.vehicle.vin)
        self.success_url += form.instance.vehicle.vin
        return super(RequestInspectionUpdateView, self).form_valid(form)


def create_request_inspection_pdf(request, vin, pk):
    request_inspection = RequestInspection.objects.get(pk=pk)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    human_readable_datetime = request_inspection.request_date.strftime(
        "%Y_%m_%d")
    response['Content-Disposition'] = 'attachment; filename=' \
        + human_readable_datetime \
        + '_Request_Inspection_' + vin + '.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    start = height - 100
    line = 15

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, start, "Your request for a vehicle inspection "
                 "is outlined below:")

    p.drawString(100, start - line * 2, "Vehicle:")
    p.drawString(100, start - line * 3,
                 "VIN:  " + vin
                 + "    Make:  " + request_inspection.vehicle.make
                 + "   Model:  " + request_inspection.vehicle.model
                 + "   Year:  " + str(request_inspection.vehicle.year))

    p.drawString(100, start - line * 5, "Seller:")
    p.drawString(100, start - line * 6,
                 "Email:  " + request_inspection.seller.email
                 + "    First name:  " + request_inspection.seller.first_name
                 + "    Last name:  " + request_inspection.seller.last_name)

    # needs human readable date
    p.drawString(100, start - line * 8,
                 "Request date:  " + str(request_inspection.request_date))

    p.drawString(100, start - line * 11, "Signature:  ______________________")

    p.drawString(100, 100, "No Lemon - nolemon.ca")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
