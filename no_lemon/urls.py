from django.conf.urls import patterns, include, url

from django.contrib import admin

from inspections.views import VehicleDetail
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'inspections.views.home_page',
        name='home'),
    url(r'^vehicles/(?P<vin>[0-9A-HJ-NPR-Z]{17})$',
        VehicleDetail.as_view(),
        name='vehicle_detail'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
