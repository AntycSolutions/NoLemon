from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from inspections.front.authenticationViews import LoginRegisterView, \
    Logout, RegisterMechanicView, \
    UpdateSellerView, UpdateMechanicView
from inspections.front.mechanics import MechanicList, MechanicDetail
from inspections.front.payments import PaymentView
from inspections.front.sellers import SellerList, SellerDetail
from inspections.front.statistics import Statistics
from inspections.front.vehicles import VehicleDetail, VehicleList, \
    VehicleCreationView
from inspections.views import InspectionList, InspectionDetail, \
    RequestInspectionUpdateView, BaseUserDetail, UpdateInspectionView
admin.autodiscover()


request_inspection_patterns = patterns(
    '',
    #     url(r'^$',
    #         RequestInspectionCreateView.as_view(),
    #         name='request_inspection_create'),
    url(r'^payment/$',
        login_required(PaymentView.as_view()),
        name='pay_for_inspection'),
    url(r'^(?P<pk>\d+)/$',
        login_required(RequestInspectionUpdateView.as_view()),
        name='request_inspection_update'),
    url(r'^(?P<pk>\d+)/print/$',
        'inspections.views.create_request_inspection_pdf',
        name='print_request_inspection')
)

vehicle_patterns = patterns(
    '',
    url(r'^new/$',
        login_required(VehicleCreationView.as_view()),
        name="vehicle_create"),
    url(r'^$',
        VehicleList.as_view(), name='vehicle_list'),
    url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})/$',
        VehicleDetail.as_view(), name='vehicle_detail'),
    url(r'^(?P<vin>[0-9a-hj-npr-z]{1,17})/request/inspection/',
        include(request_inspection_patterns)),
)

seller_patterns = patterns(
    '',
    url(r'^$',
        SellerList.as_view(), name='seller_list'),
    url(r'^(?P<pk>\d+)/$',
        SellerDetail.as_view(), name='seller_detail'),
)

mechanic_patterns = patterns(
    '',
    url(r'^$',
        MechanicList.as_view(), name='mechanic_list'),
    url(r'^(?P<pk>\d+)/$',
        MechanicDetail.as_view(), name='mechanic_detail'),
)

inspection_patterns = patterns(
    '',
    url(r'^$',
        InspectionList.as_view(), name='inspection_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(InspectionDetail.as_view()), name='inspection_detail')
)

update_patterns = patterns(
    '',
    url(r'^seller/$', UpdateSellerView.as_view(),
        name='update_seller'),
    url(r'^mechanic/$', UpdateMechanicView.as_view(),
        name='update_mechanic'),
    url(r'^inspection/(?P<pk>\d+)/$', UpdateInspectionView.as_view(),
        name='update_inspection')
)

registration_patterns = patterns(
    '',
    url(r'^$',
        LoginRegisterView.as_view(),
        name='register'),
    url(r'^mechanic/$',
        RegisterMechanicView.as_view(),
        name='register_mechanic'),
)

payment_patterns = patterns(
    '',
    url(r'^$', PaymentView.as_view(), name='payment'),
)

urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$', 'inspections.views.home_page', name='home'),
    url(r'^about/$', 'inspections.views.about_page', name='about'),
    url(r'^contact/$', 'inspections.views.contact_page', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include(registration_patterns)),
    url(r'^update/', include(update_patterns)),
    url(r'^login/$', LoginRegisterView.as_view(), name='login'),
    url(r'^logout/$', login_required(Logout.as_view()), name='logout'),
    url(r'^vehicles/', include(vehicle_patterns)),
    url(r'^inspections/', include(inspection_patterns)),
    url(r'^sellers/', include(seller_patterns)),
    url(r'^mechanics/', include(mechanic_patterns)),
    url(r'^admins/(?P<pk>.+)/$', BaseUserDetail.as_view(),
        name='base_user_detail'),
    url(r'^statistics/$', Statistics.as_view(), name='statistics'),
    #     url(r'^payments/', include(payment_patterns)),
    url(r'^requests/', include(request_inspection_patterns)),
    url(r'^email/(?P<email>.+)/$', 'inspections.views.test_email',
        name='test_email'),
    url(r'^video/$', 'inspections.views.test_video',
        name='test_video')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
