from django import template

register = template.Library()

@register.filter
def float_subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def floatval(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def absval(value):
    try:
        return __builtins__['abs'](float(value))
    except (ValueError, TypeError):
        return ''