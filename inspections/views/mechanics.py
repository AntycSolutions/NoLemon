from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView

from ..models import Mechanic


class MechanicList(ListView):
    template_name = "mechaniclist.html"
    model = Mechanic
    context_object_name = "mechanics"

    def get_context_data(self, **kwargs):
        context = super(MechanicList, self).get_context_data(**kwargs)
        context["intera_map"] = []
        for mechanic in self.get_queryset():
            full_address = mechanic.full_address().replace(" ", "+")
            context["intera_map"] += [full_address]
        return context


class MechanicDetail(DetailView):
    template_name = "mechanicdetail.html"
    model = Mechanic

    def get_context_data(self, **kwargs):
        context = super(MechanicDetail, self).get_context_data(**kwargs)
        full_address = self.object.full_address().replace(" ", "+")
        context["intera_map"] = full_address
        return context

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)

            inspections_pend = self.object.inspection_set.filter(
                Q(video="") | Q(report=""))
            inspections_comp = self.object.inspection_set.filter(
                ~Q(video=""), ~Q(report=""))

            self.context['inspections_pend'] = inspections_pend
            self.context['inspections_comp'] = inspections_comp
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any mechanics "
                "you're looking for.")
            return redirect(reverse_lazy('mechanic_list'), self.context)
        return self.render_to_response(self.context)
