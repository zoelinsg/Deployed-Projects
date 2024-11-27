from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    自定義過濾器，用於乘法運算
    """
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''