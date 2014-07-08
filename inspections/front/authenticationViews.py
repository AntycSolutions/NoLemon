from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView, View

from inspections.forms.registration import SellerCreationForm


class RegisterSellerView(FormView):
    template_name = 'testregistration.html'
    form_class = SellerCreationForm
    success_url = '/'

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        user = form.save()

        user.set_password(user.password)
        user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth_login(self.request, user)
#         user = authenticate(username=self.request.POST['email'],
#                             password=self.request.POST['password'])

        return super(RegisterSellerView, self).form_valid(form)


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
