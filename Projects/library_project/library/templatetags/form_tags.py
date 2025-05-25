from django import template

register = template.Library()

@register.filter(name='attr')
def set_attr(field, attr_string):
    """
    Set specified attributes on a form field.
    
    Example usage:
    {{ form.field|attr:"class:form-control,placeholder:Enter text" }}
    """
    attrs = {}
    pairs = attr_string.split(',')
    
    for pair in pairs:
        key, value = pair.split(':')
        attrs[key] = value
    
    return field.as_widget(attrs=attrs)