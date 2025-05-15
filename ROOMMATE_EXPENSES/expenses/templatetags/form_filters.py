from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Add a CSS class to the specified form field."""
    return field.as_widget(attrs={"class": css_class})