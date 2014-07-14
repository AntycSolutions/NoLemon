from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms.rating import RatingForm
from .models import Vehicle, Inspection, Seller, Customer, Rating


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
    context_object_name = "inspection"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.INFO,
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
    context_object_name = "seller"
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
        except:
            pass
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.INFO,
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
            self.request, messages.INFO,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += form.instance.seller.email
        return super(RatingFormCreateView, self).form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(
                    self.request, messages.INFO,
                    form.fields[field].label
                    + ". " + error)
        return redirect('/sellers/' + form.instance.seller.email)


class RatingFormUpdateView(UpdateView):
    model = Rating
    fields = ['rating']
    success_url = '/sellers/'

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += form.instance.seller.email
        return super(RatingFormUpdateView, self).form_valid(form)

# class RatingFormDeleteView(DeleteView):
#     model = Rating
#     success_url = reverse_lazy(#fix me)
