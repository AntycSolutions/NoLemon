from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client, TestCase

from inspections.models import Seller
from inspections.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('testindex.html')
        self.assertEqual(response.content.decode(), expected_html)


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_user_can_register(self):
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register Here')

        response = self.client.post('/register/',
                                    {'email': 'test@seller.ca',
                                     'password1': 'test',
                                     'password2': 'test',
                                     'first_name': 'Test',
                                     'last_name': 'Man'},
                                    follow=True)

        self.assertRedirects(response, '/')

    def test_seller_can_login(self):
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login Here')

        response = self.client.post('/register/',
                                    {'username': 'test@seller.ca',
                                     'password': 'test'},
                                    follow=True)

        self.assertRedirects(response, '/')
