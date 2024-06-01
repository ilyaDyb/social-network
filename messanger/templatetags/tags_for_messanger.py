from django import template

register = template.Library()

@register.filter
def get_name(value):
    return value.split("/")[-1].strip()