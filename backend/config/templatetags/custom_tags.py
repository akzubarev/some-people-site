"""Length_is filter for deprecated jazzmin templates."""
from django import template

register = template.Library()


@register.filter(is_safe=False)
def length_is(value, arg):
    """Whether the value's length is the argument."""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return ""
