from django import forms
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponsePermanentRedirect
from django.views.generic.edit import CreateView
import stripe

from inspections.forms.request_inspection import RequestInspectionForm
from inspections.models import RequestInspection


class PaymentView(CreateView):

    model = RequestInspection
    success_url = '/vehicles/'
    form_class = RequestInspectionForm
    template_name = 'testpayment.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        kwargs['vehicle'] = request.GET['vehicle']
        context = self.get_context_data(**kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        context['form'] = form

        print(request.GET)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        return context

    def get_form(self, form_class):
        form = form_class(**self.get_form_kwargs())
        form.fields['seller'].widget = forms.HiddenInput()
        form.fields['vehicle'].widget = forms.HiddenInput()
        form.fields['request_date'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        vin = request.POST['vehicle']
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
        paid = True
        request.session['vehicle'] = vin
        return HttpResponsePermanentRedirect(reverse('request_inspection_create'))
