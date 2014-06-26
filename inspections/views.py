from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import generics


def home_page(request):
    return render(request, 'index.html')


class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    pass