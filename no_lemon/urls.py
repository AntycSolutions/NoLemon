from django.conf.urls import patterns, include, url
from django.contrib import admin

import registration.backends.default.urls as reg_patterns

# from inspections.views.registration import RegisterSellerView


admin.autodiscover()


vehiclepatterns = patterns('',
)

# registrationpatterns = patterns('',
#     url(r'^seller$', RegisterSellerView.as_view(), name='register_seller'),
# )

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inspections.views.home_page', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(reg_patterns)),
    # url(r'^register/', include(registrationpatterns)),
    url(r'^vehicles/', include(vehiclepatterns)),
)
