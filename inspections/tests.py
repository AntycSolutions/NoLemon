from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from inspections.views import home_page, VehicleDetail



class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
         
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('index.html')
        self.assertEqual(response.content.decode(), expected_html)
        

class VehiclePageTest(TestCase):
    
    def test_vehicle_detail_url_resolves_to_vehicle_detail_view(self):
        found = resolve('/vehicles/A1B2C3D4E5F6G7H8I')
        self.assertEqual(found.func, VehicleDetail.as_view())