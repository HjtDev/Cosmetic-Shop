from django import template

register = template.Library()


@register.simple_tag
def comment_star(rating):
    return range(rating)


@register.simple_tag
def comment_o_star(rating):
    return range(5 - rating)


@register.filter
def intcomma(value):
    return f'{value:,}'
