from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.views.registration import RegisterSellerView


admin.autodiscover()


vehiclepatterns = patterns('',
)

registrationpatterns = patterns('',
    url(r'^seller$', RegisterSellerView.as_view(), name='register_seller'),
)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inspections.views.views.home_page', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include(registrationpatterns)),
    url(r'^vehicles/', include(vehiclepatterns)),
)
