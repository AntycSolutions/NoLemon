from django.contrib.auth import login
from django.views.generic import FormView

from inspections.forms import SellerCreationForm


class RegisterSellerView(FormView):
    template_name = 'testregister.html'
    form_class = SellerCreationForm
    success_url = '/'

    def form_valid(self, form):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        user = form.save()

        user.set_password(user.password)
        user.save()

        login(self.request, user)

        return super(RegisterSellerView, self).form_valid(form)
