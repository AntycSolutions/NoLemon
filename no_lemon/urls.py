from django.conf.urls import patterns, include, url

from django.contrib import admin

from inspections.views import *
admin.autodiscover()


vehiclepatterns = patterns('',
    url(r'^$', VehicleList.as_view(), name='vehicle_list'),
)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inspections.views.home_page', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^vehicles/', include(vehiclepatterns)),
)
