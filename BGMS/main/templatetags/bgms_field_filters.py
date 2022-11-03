from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    if (field.field.__class__.__name__ is 'ModelChoiceField'):
        return 'ForeignKey'
    elif (field.field.__class__.__name__ is 'ModelMultipleChoiceField'):
        return 'ManyToManyKey'
    return field.field.widget.__class__.__name__


@register.filter(name='max_length')
def max_length(field):
    return field.field.widget.attrs.get('maxlength')