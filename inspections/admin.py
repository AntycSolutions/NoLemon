from django.contrib import admin
from django.contrib.auth.models import Group

from inspections.forms.registration import BaseUserAdmin
from inspections.models import BaseUser, Seller, Customer, Vehicle, Inspection


# Now register the new UserAdmin...
admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Inspection)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)