from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.front.authenticationViews import RegisterSellerView, Login, \
    Logout
admin.autodiscover()


vehiclepatterns = patterns('',
                           )

registrationpatterns = patterns('',
                                url(r'^seller$', RegisterSellerView.as_view(),
                                    name='register_seller'),
                                )

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'inspections.views.home_page', name='home'),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^register/', include(registrationpatterns)),
                       url(r'^login/$', Login.as_view(), name='login'),
                       url(r'^logout/$', Logout.as_view(), name='logout'),
                       url(r'^vehicles/', include(vehiclepatterns)),
                       )
