from django import template

register = template.Library()

@register.filter
def pages_list(value):
    return list(range(1, value + 1))