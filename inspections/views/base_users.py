from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView

from ..models import BaseUser, InspectionRequest, Inspection


class BaseUserDetail(DetailView):
    template_name = 'base_user/baseuserdetail.html'
    model = BaseUser

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any admins "
                "you're looking for.")
            return redirect(reverse_lazy('home'), self.context)
        self.context['inspection_requests'] = InspectionRequest.objects.all()
        self.context['inspections_pend'] = Inspection.objects.filter(
            vehicle_history="")
        self.context['inspections_comp'] = Inspection.objects.filter(
            ~Q(vehicle_history=""))
        self.context['base_users'] = BaseUser.objects.filter(
            is_active=False)
        return self.render_to_response(self.context)
