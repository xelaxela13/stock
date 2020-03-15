from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_context_data_by_name(context, name):
    return context.get(name)
