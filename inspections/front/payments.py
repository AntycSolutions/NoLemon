from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponsePermanentRedirect
from django.views.generic import TemplateView
import stripe

from inspections.models import Vehicle


class PaymentView(TemplateView):

    template_name = 'testpayment.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        vin = request.GET['vehicle']
        vehicle = Vehicle.objects.get(vin=vin)
        context['vehicle'] = vehicle
        return self.render_to_response(context)

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
