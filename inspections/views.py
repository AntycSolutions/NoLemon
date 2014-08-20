from django.contrib import messages
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, UpdateView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms.request_inspection import RequestInspectionForm
from .forms.video import VideoForm
from .models import Inspection, InspectionRequest, Mechanic, Vehicle


def home_page(request):
    return render(request, 'index.html')


def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    return render(request, 'contact.html')


class InspectionList(ListView):
    template_name = "old/testinspectionlist.html"
    model = Inspection
    context_object_name = "inspections"


class InspectionDetail(DetailView):
    template_name = "old/testinspectiondetail.html"
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
            return redirect(reverse_lazy('inspections_list'), self.context)
        return self.render_to_response(self.context)


# class RequestInspectionCreateView(CreateView):
#
#     pass


class RequestInspectionUpdateView(UpdateView):
    model = InspectionRequest
    success_url = reverse_lazy('vehicle_list')
    form_class = RequestInspectionForm

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully updated a request for an inspection for "
            + form.instance.vehicle.vin)
        self.success_url += form.instance.vehicle.vin
        return super(RequestInspectionUpdateView, self).form_valid(form)


def create_request_inspection_pdf(request, vin, pk):
    request_inspection = InspectionRequest.objects.get(pk=pk)

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
    human_readable_request_datetime = request_inspection.request_date.strftime(
        "%Y-%m-%d %H:%M:%S")
    p.drawString(100, start - line * 8,
                 "Request date:  "
                 # 2014-07-25 20:11:36
                 + human_readable_request_datetime)

    p.drawString(100, start - line * 11, "Signature:  ______________________")

    p.drawString(100, 100, "No Lemon - nolemon.ca")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def test_email(request, email):
    emails = [{'email': email}]
    send_email(emails)
    return HttpResponse("Email sent.")


def send_email(emails):
    title = "NoLemon - Inspection Request"
    content = "An inspection request has been made. Please approve.\n"

    datatuple = []
    for email in emails:
        datatuple.append((title, content, 'NoLemon <no-reply@nolemon.ca>',
                          [email['email']]))

    send_mass_mail(datatuple, fail_silently=False)


def test_video(request):
    # Handle file upload
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            newVideo = Inspection(
                comments=request.POST['comments'],
                date=request.POST['date'],
                views=request.POST['views'],
                mechanic=Mechanic.objects.get(pk=request.POST['mechanic']),
                vehicle=Vehicle.objects.get(pk=request.POST['vehicle']),
                video=request.FILES['video'])
            newVideo.save()

            # Redirect to the video list after POST
            return HttpResponseRedirect(reverse('test_video'))
    else:
        # An empty, unbound form
        form = VideoForm()

    # Load videos for the list page
    inspections = Inspection.objects.all()

    # Render list page with the videos and the form
    return render_to_response(
        'video.html',
        {'inspections': inspections, 'form': form},
        context_instance=RequestContext(request)
    )
