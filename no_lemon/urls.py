from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from inspections.views.authenticationViews import LoginRegisterView, \
    Logout, RegisterMechanicView, \
    UpdateSellerView, UpdateMechanicView, UpdateBaseUserView
from inspections.views.mechanics import MechanicList, MechanicDetail
from inspections.views.payments import PaymentView, PayToView
from inspections.views.sellers import SellerList, SellerDetail
from inspections.views.statistics import Statistics
from inspections.views.vehicles import VehicleDetail, VehicleList, \
    VehicleCreationView, UpdateVehicleView
from inspections.views.base_users import BaseUserDetail
from inspections.views.inspection import InspectionDetail, \
    UpdateInspectionView, CreateInspectionView
from inspections.views.views import RequestInspectionUpdateView
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
        'inspections.views.views.create_request_inspection_pdf',
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
    # url(r'^$',
    #     InspectionList.as_view(), name='inspection_list'),
    url(r'^create/(?P<pk>\d+)/$',
        login_required(CreateInspectionView.as_view()),
        name='create_inspection'),
    url(r'^(?P<pk>\d+)/(?P<receipt>\w+)/$',
        InspectionDetail.as_view(), name='inspection_detail')
)

update_patterns = patterns(
    '',
    url(r'^seller/$', UpdateSellerView.as_view(),
        name='update_seller'),
    url(r'^mechanic/$', UpdateMechanicView.as_view(),
        name='update_mechanic'),
    url(r'^base_user/$', UpdateBaseUserView.as_view(),
        name='update_base_user'),
    url(r'^inspection/(?P<pk>\d+)/$', UpdateInspectionView.as_view(),
        name='update_inspection'),
    url(r'^vehicle/(?P<pk>\d+)/$', UpdateVehicleView.as_view(),
        name='update_vehicle')
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
    url(r'^view/', PayToView.as_view(), name='pay_to_view'),
)

urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$', 'inspections.views.views.home_page', name='home'),
    url(r'^about/$', 'inspections.views.views.about_page', name='about'),
    url(r'^contact/$', 'inspections.views.views.contact_page', name='contact'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', include(registration_patterns)),
    url(r'^update/', include(update_patterns)),
    url(r'^login/$', LoginRegisterView.as_view(), name='login'),
    url(r'^logout/$', login_required(Logout.as_view()), name='logout'),
    url(r'^vehicles/', include(vehicle_patterns)),
    url(r'^inspections/', include(inspection_patterns)),
    url(r'^sellers/', include(seller_patterns)),
    url(r'^mechanics/', include(mechanic_patterns)),
    url(r'^admins/(?P<pk>.+)/$', login_required(BaseUserDetail.as_view()),
        name='base_user_detail'),
    url(r'^statistics/$', Statistics.as_view(), name='statistics'),
    url(r'^payments/', include(payment_patterns)),
    url(r'^requests/', include(request_inspection_patterns)),
    url(r'^email/(?P<email>.+)/$', 'inspections.views.views.test_email',
        name='test_email'),
    url(r'^video/$', 'inspections.views.views.test_video',
        name='test_video')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
