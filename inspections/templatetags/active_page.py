# http://stackoverflow.com/questions/19268727
#  /django-how-to-get-the-name-of-the-template-being-rendered

from django import template
register = template.Library()


@register.simple_tag
def active_page(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        #print (resolve(request.path_info).url_name)
        if resolve(request.path_info).url_name == view_name:
            return "active"
        else:
            return ""
    except Resolver404:
        return ""
