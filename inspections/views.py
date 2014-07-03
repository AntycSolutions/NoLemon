from django.contrib import messages
from django.contrib.admin.util import lookup_field
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from inspections.models import Inspection, Vehicle, Seller


def home_page(request):
    return render(request, 'testindex.html')


class VehicleList(generics.ListCreateAPIView):
    model = Vehicle
    template_name = "testvehiclelist.html"
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, *args, **kwargs):
        super(VehicleList, self).get(request, *args, **kwargs)
        
        vehicles = Vehicle.objects.all()
        self.context = {'vehicles': vehicles}
        
        return Response(self.context)


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Vehicle
    lookup_field = 'vin'
    template_name = "testvehicleinspection.html"
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, *args, **kwargs):
        super(VehicleDetail, self).get(request, *args, **kwargs)
        self.context = {}
        try:
            self.vehicle = self.get_object()
            self.context['vehicle'] = self.vehicle
        except:
            messages.add_message(request, messages.INFO, "We're sorry, we don't seem to have any inspections for the vehicle you're looking for.")
            return redirect('/vehicles', self.context)
            
        return Response(self.context)
    

class InspectionList(generics.ListCreateAPIView):
    model = Inspection
    
    
class SellerList(generics.ListCreateAPIView):
    model = Seller