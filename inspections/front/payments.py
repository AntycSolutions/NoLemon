import datetime

from django import forms
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from inspections.forms.request_inspection import RequestInspectionForm
from inspections.models import InspectionRequest, Seller, Vehicle,\
    Mechanic, Receipt
from inspections.utilities import process_stripe, send_email
from no_lemon import settings


class PaymentView(CreateView):

    model = InspectionRequest
    success_url = reverse_lazy('vehicle_list')
    form_class = RequestInspectionForm
    template_name = 'requestinspection.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        vin = kwargs['vin'] if 'vin' in kwargs else request.GET['vehicle']
        vehicle = Vehicle.objects.get(vin=vin)
        seller = Seller.objects.get(email=request.user.email)

        form = RequestInspectionForm(initial={
            'seller': seller,
            'vehicle': vehicle,
            'request_date': datetime.datetime.now()}
        )
        form.fields['seller'].widget = forms.HiddenInput()
        form.fields['vehicle'].widget = forms.HiddenInput()
        form.fields['mechanic'].widget = forms.HiddenInput()
        form.fields['request_date'].widget = forms.HiddenInput()

        return self.render_to_response(self.get_context_data(form=form,
                                                             vehicle=vehicle))

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["intera_map"] = []
        context["mechanics"] = Mechanic.objects.all()
        label = 65
        for mechanic in context["mechanics"]:
            full_address = mechanic.full_address().replace(" ", "+")
            context["intera_map"] += [full_address]
#             context["static_map"] += "markers="
#             context["static_map"] += "label:" + chr(label) + "|"
#             context["static_map"] += full_address + "&"
            mechanic.label = chr(label)
            label += 1
#         context["static_map"] = context["static_map"][:-1]
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        # TODO: Integrate payment level options
        cost = settings.INSPECTION_REQUEST

        process_stripe(request.POST['stripeToken'], cost)

        return super(PaymentView, self).post(request, args, kwargs)

    def form_valid(self, form):
        #         admin_emails = BaseUser.objects.filter(is_admin=True).values('email')
        #         self._send_email(admin_emails)
        send_email()
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully requested an inspection for "
            + form.instance.vehicle.__str__() + ". " +
            "You will be contacted by a NoLemon administrator " +
            "within 1 business days to confirm your request.")
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
        return redirect(reverse_lazy('request_inspection_create',
                                     kwargs={'vin': form.instance.vehicle.vin}
                                     ))

    def _send_email(self, emails):
        title = "NoLemon - Inspection Request"
        content = "An inspection request has been made. Please approve.\n"

        datatuple = []
        for email in emails:
            datatuple.append((title, content, 'NoLemon <no-reply@nolemon.ca>',
                              [email['email']]))

        send_mass_mail(datatuple, fail_silently=False)


class PayToView(CreateView):
    template_name = "payment.html"
    success_url = "/"
    model = Receipt

    def post(self, request, *args, **kwargs):
        print("You talkin'a me?? With this?? ")
        print(request.POST)
        return super(PayToView, self).post(request, *args, **kwargs)