from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView, View, UpdateView

from ..forms.registration import SellerCreationForm, \
    MechanicCreationForm
from ..models import Seller, Mechanic


class LoginRegisterView(FormView):
    template_name = 'testloginregister.html'
    form_class = SellerCreationForm
    second_form_class = AuthenticationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(LoginRegisterView, self).get_context_data(**kwargs)
        if 'reg_form' not in context:
            context['reg_form'] = self.form_class()
        if 'login_form' not in context:
            context['login_form'] = self.second_form_class()
        return context

    def form_valid(self, form):
        if (form.__class__ == SellerCreationForm):
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
                else:
                    # Return a 'disabled account' error message
                    print("account inactive")
            else:
                # Return an 'invalid login' error message.
                print("user not authenticated")

        else:
                #         redirect_to = settings.LOGIN_REDIRECT_URL
            auth_login(self.request, form.get_user())
            if self.request.session.test_cookie_worked():
                self.request.session.delete_test_cookie()

        return super(LoginRegisterView, self).form_valid(form)

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        # get the user instance
        #         self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'reg_form' in request.POST:

            # get the primary form
            form_class = self.get_form_class()
            form_name = 'reg_form'

        else:

            # get the secondary form
            form_class = self.second_form_class
            form_name = 'login_form'

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})


class UpdateSellerView(UpdateView):
    template_name = 'testupdate.html'
    model = Seller
    fields = ['first_name', 'last_name', ]

    def get_object(self):
        seller = None
        try:
            seller = Seller.objects.get(email=self.request.user.email)
        except:
            pass
        return seller

    def get(self, request):
        self.object = self.get_object()
        if not self.object:
            return redirect('/')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form, url_end='seller')
        )


class RegisterMechanicView(FormView):
    template_name = 'testregistration.html'
    form_class = MechanicCreationForm
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
            else:
                # Return a 'disabled account' error message
                print("account inactive")
        else:
            # Return an 'invalid login' error message.
            print("user not authenticated")

        return super(RegisterMechanicView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        print("The Post info: ")
        print(request.POST)
        return FormView.post(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  url_end='mechanic')
        )


class UpdateMechanicView(UpdateView):
    template_name = 'testupdate.html'
    model = Mechanic
    fields = ['first_name', 'last_name',
              'address', 'city', 'province', ]

    def get_object(self):
        mechanic = None
        try:
            mechanic = Mechanic.objects.get(email=self.request.user.email)
        except:
            pass
        return mechanic

    def get(self, request):
        self.object = self.get_object()
        if not self.object:
            return redirect('/')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form, url_end='mechanic')
        )


class Logout(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
