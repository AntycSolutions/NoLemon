# http://vanderwijk.info/blog
# /adding-css-classes-formfields-in-django-templates/

from django import template
register = template.Library()


@register.filter
def addcss(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)


@register.filter
def gettype(field):
    return field.field.widget.__class__.__name__


@register.filter
def is_number(type):
    return type in ["NumberInput"]


@register.filter
def is_file(type):
    return type in ["ClearableFileInput"]


@register.filter
def is_datetimepicker(type):
    return type in ["DateTimePicker"]
