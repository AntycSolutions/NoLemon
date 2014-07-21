from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.front.authenticationViews import RegisterSellerView, Login, \
    Logout, RegisterCustomerView
from inspections.front.payments import PaymentView
from inspections.front.statistics import Statistics
from inspections.views import VehicleDetail, VehicleList, \
    InspectionList, InspectionDetail, SellerList, SellerDetail, \
    RatingFormCreateView, RatingFormUpdateView, \
    RequestInspectionCreateView, RequestInspectionUpdateView, \
    MechanicList, MechanicDetail
admin.autodiscover()


request_inspection_patterns = patterns(
    '',
    url(r'^$',
        RequestInspectionCreateView.as_view(),
        name='request_inspection_create'),
    url(r'^payment/$',
        PaymentView.as_view(),
        name='pay_for_inspection'),
    url(r'^(?P<pk>\d+)/$',
        RequestInspectionUpdateView.as_view(),
        name='request_inspection_update'),
    url(r'^(?P<pk>\d+)/print/$',
        'inspections.views.create_request_inspection_pdf',
        name='print_request_inspection')
)

vehicle_patterns = patterns(
    '',
    url(r'^$',
        VehicleList.as_view(), name='vehicle_list'),
    url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})/$',
        VehicleDetail.as_view(), name='vehicle_detail'),
    url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})/request/inspection/',
        include(request_inspection_patterns))
)

seller_patterns = patterns(
    '',
    url(r'^$',
        SellerList.as_view(), name='seller_list'),
    url(r'^(?P<pk>.+)/$',
        SellerDetail.as_view(), name='seller_detail'),
)

mechanic_patterns = patterns(
    '',
    url(r'^$',
        MechanicList.as_view(), name='mechanic_list'),
    url(r'^(?P<pk>.+)/$',
        MechanicDetail.as_view(), name='mechanic_detail'),
)

rating_patterns = patterns(
    '',
    url(r'^$',
        RatingFormCreateView.as_view(), name='rating_create'),
    url(r'^(?P<pk>\d+)/$',
        RatingFormUpdateView.as_view(), name='rating_update'),
    # url(r'(?P<pk>\d+)/delete/$',
    #     RatingFormDeleteView.as_view(), name='rating_delete')
)

inspection_patterns = patterns(
    '',
    url(r'^$',
        InspectionList.as_view(), name='inspection_list'),
    url(r'^(?P<pk>\d+)/$',
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

payment_patterns = patterns(
    '',
    url(r'^$', PaymentView.as_view(), name='payment'),
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
    url(r'^mechanics/', include(mechanic_patterns)),
    url(r'^ratings/', include(rating_patterns)),
    url(r'^statistics/$', Statistics.as_view(), name='statistics'),
    #     url(r'^payments/', include(payment_patterns)),
    url(r'^requests/', include(request_inspection_patterns)),
)
