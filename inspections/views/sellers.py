from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from ..models import Seller


class SellerList(ListView):
    template_name = "old/sellerlist.html"
    model = Seller
    context_object_name = "sellers"


class SellerDetail(DetailView):
    template_name = "seller/sellerdetail.html"
    model = Seller

    def get(self, request, *args, **kwargs):
        self.context = None
        try:
            self.object = self.get_object()
            self.context = self.get_context_data(object=self.object)
        except:
            messages.add_message(
                request, messages.ERROR,
                "We're sorry, we don't seem to have any sellers "
                "you're looking for.")
            return redirect(reverse_lazy('seller_list'), self.context)
        return self.render_to_response(self.context)
