from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.front.authenticationViews import RegisterSellerView, Login, \
    Logout, RegisterCustomerView
from inspections.views import VehicleDetail, VehicleList, \
    InspectionList, InspectionDetail, SellerList, SellerDetail, \
    RatingFormCreateView, RatingFormUpdateView
from inspections.front.statistics import Statistics
admin.autodiscover()


vehicle_patterns = patterns(
    '',
    url(r'^$',
        VehicleList.as_view(), name='vehicle_list'),
    url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})',
        VehicleDetail.as_view(), name='vehicle_detail'),
    )

seller_patterns = patterns(
    '',
    url(r'^$',
        SellerList.as_view(), name='seller_list'),
    url(r'^(?P<email>.+)',
        SellerDetail.as_view(), name='seller_detail'),
    )

rating_patterns = patterns(
    '',
    url(r'^$',
        RatingFormCreateView.as_view(), name='rating_create'),
    url(r'(?P<pk>\d+)/$',
        RatingFormUpdateView.as_view(), name='rating_update'),
    # url(r'(?P<pk>\d+)/delete/$',
    #     RatingFormDeleteView.as_view(), name='rating_delete')
    )

inspection_patterns = patterns(
    '',
    url(r'^$',
        InspectionList.as_view(), name='inspection_list'),
    url(r'^(?P<pk>\d+)',
        InspectionDetail.as_view(), name='inspection_detail')
    )

registration_patterns = patterns(
    '',
    url(r'^seller/$',
        RegisterSellerView.as_view(),
        name='register_seller'),
    url(r'^customer/$',
        RegisterCustomerView.as_view(),
        name='register_customer'),
    )

urlpatterns = patterns(
    '',
    url(r'^$', 'inspections.views.home_page', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include(registration_patterns)),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^vehicles/', include(vehicle_patterns)),
    url(r'^inspections/', include(inspection_patterns)),
    url(r'^sellers/', include(seller_patterns)),
    url(r'^ratings/', include(rating_patterns)),
    url(r'^statistics/', Statistics.as_view(), name='statistics')
    )
