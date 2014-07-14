# http://michalcodes4life.wordpress.com/2014/02/08
# /multiple-user-types-in-django-1-6/

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from .models import BaseUser, Seller, Customer, Mechanic, \
    Vehicle, Inspection, Rating, RequestInspection
from .forms.registration import BaseUserCreationForm, SellerCreationForm, \
    CustomerCreationForm, MechanicCreationForm, \
    BaseUserChangeForm, SellerChangeForm, \
    CustomerChangeForm, MechanicChangeForm


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
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_admin',)
    filter_horizontal = ()
    ordering = ('email',)
    search_fields = ('email',)
    form = BaseUserChangeForm
    add_form = BaseUserCreationForm

admin.site.register(BaseUser, BaseUserAdmin)


class SellerAdmin(UserAdmin):
    list_display = ('email', 'rating')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
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


class CustomerAdmin(UserAdmin):
    list_display = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    list_filter = ('is_admin',)
    filter_horizontal = ()
    ordering = ('email',)
    search_fields = ('email',)
    form = CustomerChangeForm
    add_form = CustomerCreationForm

admin.site.register(Customer, CustomerAdmin)


class MechanicAdmin(UserAdmin):
    list_display = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name',
                       'phone_number', 'address')}
         ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'phone_number', 'address')}),
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
admin.site.register(Rating)
admin.site.register(RequestInspection)

admin.site.unregister(Group)
admin.site.unregister(Site)
