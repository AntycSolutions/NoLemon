from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from ..forms.rating import RatingForm
from ..models import Seller, Customer, Rating


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
            return redirect(reverse_lazy('seller_list'), self.context)
        return self.render_to_response(self.context)


class RatingFormCreateView(CreateView):
    model = Rating
    fields = ['rating']
    success_url = reverse_lazy('seller_list')
    form_class = RatingForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += str(form.instance.seller.pk)
        return super(RatingFormCreateView, self).form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.add_message(
                    self.request, messages.ERROR,
                    form.fields[field].label
                    + ". " + error)
        return redirect('/sellers/' + str(form.instance.seller.pk))


class RatingFormUpdateView(UpdateView):
    model = Rating
    fields = ['rating']
    success_url = reverse_lazy('seller_list')
    form_class = RatingForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully rated " + form.instance.seller.email)
        self.success_url += str(form.instance.seller.pk)
        return super(RatingFormUpdateView, self).form_valid(form)


# class RatingFormDeleteView(DeleteView):
#     model = Rating
# success_url = reverse_lazy(#fix me)
