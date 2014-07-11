from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView, View

from ..forms.registration import SellerCreationForm, \
    CustomerCreationForm


class RegisterSellerView(FormView):
    template_name = 'testregistration.html'
    form_class = SellerCreationForm
    success_url = '/'

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = form.save()

        user = authenticate(
            email=user.email,
            password=form.cleaned_data["password1"])  # get plaintext
        if user is not None:
            if user.is_active:
                auth_login(self.request, user)
                # Redirect to a success page.
                print("login success")
            else:
                # Return a 'disabled account' error message
                print ("account inactive")
        else:
            # Return an 'invalid login' error message.
            print ("user not authenticated")

        return super(RegisterSellerView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form,
                                                             url_end='seller'))


class RegisterCustomerView(FormView):
    template_name = 'testregistration.html'
    form_class = CustomerCreationForm
    success_url = '/'

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user = form.save()

        user = authenticate(
            email=user.email,
            password=form.cleaned_data["password1"])  # get plaintext
        if user is not None:
            if user.is_active:
                auth_login(self.request, user)
                # Redirect to a success page.
                print("login success")
            else:
                # Return a 'disabled account' error message
                print ("account inactive")
        else:
            # Return an 'invalid login' error message.
            print ("user not authenticated")

        return super(RegisterCustomerView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  url_end='customer')
        )


class Login(FormView):
    template_name = 'testlogin.html'
    success_url = '/'
    form_class = AuthenticationForm

    def form_valid(self, form):
        #         redirect_to = settings.LOGIN_REDIRECT_URL
        auth_login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(Login, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)


class Logout(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
