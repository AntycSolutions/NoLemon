from django import template
register = template.Library()

from inspections.models import Seller, Mechanic, BaseUser


@register.filter
def get_class(value):
    return value.__class__.__name__


@register.filter
def get_class_type(user):
    if Seller.objects.filter(pk=user.pk).count() > 0:
        return 'seller_detail'
    if Mechanic.objects.filter(pk=user.pk).count() > 0:
        return 'mechanic_detail'
    if BaseUser.objects.filter(pk=user.pk).count() > 0:
        return 'base_user_detail'
