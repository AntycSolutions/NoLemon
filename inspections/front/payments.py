import datetime

from django import forms
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
import stripe

from inspections.forms.request_inspection import RequestInspectionForm
from inspections.models import RequestInspection, Seller, Vehicle


class PaymentView(CreateView):

    model = RequestInspection
    success_url = '/vehicles/'
    form_class = RequestInspectionForm
    template_name = 'testpayment.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        vehicle = Vehicle.objects.get(vin=request.GET['vehicle'])
        seller = Seller.objects.get(email=request.user.email)

        form = RequestInspectionForm(initial={
            'seller': seller,
            'vehicle': vehicle,
            'request_date': datetime.datetime.now()}
        )
        form.fields['seller'].widget = forms.HiddenInput()
        form.fields['vehicle'].widget = forms.HiddenInput()
        form.fields['request_date'].widget = forms.HiddenInput()

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None

        self._handle_stripe(request)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return super(PaymentView, self).post(request, args, kwargs)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully requested an inspection for "
            + form.instance.seller.email)
        self.success_url += form.instance.vehicle.vin
        return super(PaymentView, self).form_valid(form)

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

    def _handle_stripe(self, request):
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account
        stripe.api_key = "sk_test_y8HvZWWtuKZAMrQsRPtRro6F"

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']

        # Create the charge on Stripe's servers - this will charge the user's
        # card
        try:
            charge = stripe.Charge.create(
                amount=20000,  # amount in cents, again
                currency="cad",
                card=token,
                description="payinguser@example.com"
            )
        except stripe.CardError as e:
            # The card has been declined
            return Http404()
