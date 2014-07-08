from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.front.authenticationViews import RegisterSellerView, Login, \
    Logout, RegisterCustomerView
from inspections.views import VehicleDetail, VehicleList
admin.autodiscover()


vehiclepatterns = patterns('',
                           url(r'^$', VehicleList.as_view(),
                               name='vehicle_list'),
                           url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})',
                               VehicleDetail.as_view(),
                               name='vehicle_detail'),
                           )

registrationpatterns = patterns('',
                                url(r'^seller$',
                                    RegisterSellerView.as_view(),
                                    name='register_seller'),
                                url(r'^customer$',
                                    RegisterCustomerView.as_view(),
                                    name='register_customer'),
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
