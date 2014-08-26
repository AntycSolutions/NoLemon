# http://michalcodes4life.wordpress.com/2014/02/08
# /multiple-user-types-in-django-1-6/

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from .forms.registration import BaseUserCreationForm, \
    SellerCreationForm, MechanicCreationForm, \
    BaseUserChangeForm, SellerChangeForm, \
    MechanicChangeForm
from .models import BaseUser, Seller, Mechanic, \
    Vehicle, Inspection, InspectionRequest, Receipt


class BaseUserAdmin(UserAdmin):
    list_display = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password', 'id')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_admin',)
    filter_horizontal = ()
    ordering = ('email',)
    search_fields = ('email',)
    readonly_fields = ('id',)
    form = BaseUserChangeForm
    add_form = BaseUserCreationForm

admin.site.register(BaseUser, BaseUserAdmin)


class SellerAdmin(UserAdmin):
    list_display = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'city')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'city'
                                         )}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_admin',)
    filter_horizontal = ()
    ordering = ('email',)
    search_fields = ('email',)
    form = SellerChangeForm
    add_form = SellerCreationForm

admin.site.register(Seller, SellerAdmin)


class MechanicAdmin(UserAdmin):
    list_display = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name',
                       'phone_number', 'address', 'city', 'province')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'phone_number', 'address',
                                         'city', 'province')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_admin',)
    filter_horizontal = ()
    ordering = ('email',)
    search_fields = ('email',)
    form = MechanicChangeForm
    add_form = MechanicCreationForm

admin.site.register(Mechanic, MechanicAdmin)

admin.site.register(Vehicle)
admin.site.register(Inspection)
admin.site.register(InspectionRequest)
admin.site.register(Receipt)

admin.site.unregister(Group)
admin.site.unregister(Site)
