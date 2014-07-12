from django.views.generic import TemplateView

from ..models import Mechanic, Seller, Inspection


class Statistics(TemplateView):
    template_name = "statistics.html"
    context = dict()

    def get(self, request, *args, **kwargs):
        #number of mechanics, number of inspection videos and views,
        #number of sellers, etc.
        mechanicsTotal = Mechanic.objects.all().count()
        sellersTotal = Seller.objects.all().count()
        inspectionsTotal = Inspection.objects.all().count()
        viewsTotal = 0
        for i in Inspection.objects.all():
            viewsTotal += i.views

        self.context['mechanicsTotal'] = mechanicsTotal
        self.context['sellersTotal'] = sellersTotal
        self.context['inspectionsTotal'] = inspectionsTotal
        self.context['viewsTotal'] = viewsTotal

        return self.render_to_response(self.context)
