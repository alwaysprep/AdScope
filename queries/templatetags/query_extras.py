from django import template


register = template.Library()


@register.filter(name='percent')
def percent(value, arg):
    return ( value + arg ) * 5
