from django.views.generic import RedirectView
import stripe


class PaymentView(RedirectView):

    url = '/'

    def post(self, request, *args, **kwargs):
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
            pass
        return RedirectView.post(self, request, *args, **kwargs)
