from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from ..models import Inspection, Receipt, BaseUser, Mechanic, InspectionRequest
from ..forms.inspection import InspectionUpdateForm, InspectionCreateForm


class InspectionList(ListView):
    template_name = "old/testinspectionlist.html"
    model = Inspection
    context_object_name = "inspections"


class InspectionDetail(DetailView):
    template_name = "inspection/inspectiondetail.html"
    model = Inspection

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any inspections "
                "you're looking for.")
            return redirect(reverse_lazy('vehicle_list'), self.context)
        try:
            Receipt.objects.get(inspection=self.object,
                                number=self.kwargs['receipt'])
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, the receipt number that was entered was "
                "incorrect.")
            vehicle_vin = self.object.vehicle.vin
            return redirect(reverse_lazy('vehicle_detail',
                                         kwargs={'vin': vehicle_vin}),
                            self.context)
        return self.render_to_response(self.context)


class UpdateInspectionView(UpdateView):
    template_name = 'update.html'
    model = Inspection
    form_class = InspectionUpdateForm

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            return reverse('update_inspection', kwargs={'pk': pk})

    def get(self, request, **kwargs):
        try:
            # Check if mechanic is updating inspection first as it's more
            #  common, then check if admin is updating inspection
            Mechanic.objects.get(email=self.request.user.email)
            return self._get()
        except:
            try:
                base_user = BaseUser.objects.get(email=self.request.user.email)
                if base_user.is_admin:
                    return self._get()
                else:
                    raise
            except:
                messages.add_message(
                    request, messages.ERROR,
                    "We're sorry, only mechanics or admins can update"
                    " inspection reports.")
                return redirect(reverse_lazy('home'))

    def _get(self):
        self.object = self.get_object()
        if not self.object:
            return redirect('/')
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form.fields['vehicle'].widget.attrs['readonly'] = True
        form.fields['mechanic'].widget.attrs['readonly'] = True
        form.fields['views'].widget.attrs['readonly'] = True

        context = self.get_context_data(form=form)
        context['model_type'] = 'Inspection'
        context['form_type'] = 'multipart/form-data'

        return self.render_to_response(context)


class CreateInspectionView(CreateView):  # DERP
    model = Inspection
    form_class = InspectionCreateForm
    template_name = 'inspection/inspectioncreate.html'

    def get_success_url(self):
        bu = BaseUser.objects.get(email=self.request.user.email)
        self.success_url = reverse_lazy('base_user_detail',
                                        kwargs={'pk': bu.pk})
        return self.success_url

    def get_initial(self, **kwargs):
        initial = super(CreateInspectionView, self).get_initial()
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            inspection_request = InspectionRequest.objects.get(pk=pk)
            initial['vehicle'] = inspection_request.vehicle
            initial.update({'inspection_request_pk': pk})
        return initial

    def form_valid(self, form):
        pk = self.kwargs['pk']
        InspectionRequest.objects.get(pk=pk).delete()
        return super(CreateInspectionView, self).form_valid(form)
